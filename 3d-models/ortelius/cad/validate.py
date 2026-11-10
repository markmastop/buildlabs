"""Onafhankelijke hercontrole van geëxporteerde STEP, STL en geometrie-3MF."""
from pathlib import Path
import json, zipfile, xml.etree.ElementTree as ET, hashlib
import numpy as np
import cadquery as cq
import trimesh
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'print/onderdelen.json').read_text());results=[];shapes={};meshes={}
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
for q in D['parts']:
 n=q['name'];stl=R/'print/stl'/(n+'.stl');step=R/'cad/step'/(n+'.step');mf=R/'print/3mf'/(n+'.3mf')
 m=trimesh.load_mesh(stl,process=True);s=cq.importers.importStep(str(step)).val();shapes[n]=s;meshes[n]=m
 assert len(s.Solids())==1 and s.isValid(),(n,'STEP')
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0,(n,'STL')
 assert np.isfinite(m.vertices).all() and max(m.extents)<=246.001,(n,'P2S')
 assert np.min(m.bounds[0])>=-.001 and np.max(np.abs(m.bounds[0]))<.06,(n,'bed-oorsprong')
 delta=abs(s.Volume()-m.volume)/m.volume;assert delta<.015,(n,'STEP/STL volume',delta)
 with zipfile.ZipFile(mf) as z:
  assert z.testzip() is None
  root=ET.fromstring(z.read('3D/3dmodel.model'));assert root.attrib['unit']=='millimeter'
  vs=np.array([[float(v.attrib[k]) for k in ['x','y','z']] for v in root.findall('.//m:vertex',NS)])
  fs=np.array([[int(v.attrib[k]) for k in ['v1','v2','v3']] for v in root.findall('.//m:triangle',NS)])
  assert np.allclose(m.vertices,vs,atol=1e-6) and np.array_equal(m.faces,fs),(n,'3MF gelijk aan STL')
  tr=list(map(float,root.find('m:build/m:item',NS).attrib['transform'].split()))
  assert np.allclose(tr[:9],[1,0,0,0,1,0,0,0,1])
  placed=vs+tr[9:];assert np.min(placed[:,:2])>=5 and np.max(placed[:,:2])<=251,(n,'3MF-plaatpositie')
 results.append(dict(part=n,STEP_valid=True,STL_closed=True,one_component=True,P2S_margin_mm=round((256-max(m.extents))/2,3),STEP_STL_volume_delta=round(delta,6),geometry_3MF_matches_STL=True))
 print(n,'HERCONTROLE OK',flush=True)
# Printbestanden staan op bed; inverse exporttransformatie herstelt hun assemblagepositie.
def world(q):
 s=shapes[q['name']].translate(cq.Vector(*[-x for x in q['bed_translation']]))
 if q['rotation']:s=s.rotate((0,0,0),q['rotation'][0],-q['rotation'][1])
 return s
worlds={q['name']:world(q) for q in D['parts']}
hull=[worlds['01_romp_'+str(i)] for i in range(1,5)]
rc_collisions=[]
for q in D['parts']:
 if q['group']!='RC' or not q['included']:continue
 for p in q['assembly_translations']:
  s=worlds[q['name']].translate(cq.Vector(*p));v=sum(s.intersect(h).Volume() for h in hull)
  assert v<.1,(q['name'],p,'RC raakt romp',v)
  rc_collisions.append(dict(part=q['name'],translation=p,intersection_mm3=round(v,6)))
# Schroefmal en roer mogen elkaar niet raken (roer staat achter de schroef).
assert worlds['57_schroefmal_40'].intersect(worlds['56_roerblad']).Volume()<.01,'roer raakt schroefcirkel'
# Controleer lijmstroken versus romp en achterste vloer; raakvlakken hebben geen volume.
for i in range(1,4):
 n='02_lasstrook_'+str(i);s=worlds[n]
 v=sum(s.intersect(h).Volume() for h in hull)
 assert v<.1,(n,'strook snijdt romp',v)
 assert s.intersect(worlds['03_werkdek_achter']).Volume()<.1
# Achterste serviceluik moet vrij in de vaste dekopening vallen.
assert worlds['03_serviceluik_achter'].intersect(worlds['03_werkdek_achter']).Volume()<.01
# Reële raamgaten en galerieopeningen blijven na STEP-herimport open.
for n,point in [('16_galerijwand_BB',(445,78,183)),('16_galerijwand_SB',(445,-78,183)),('17_brug',(695,0,212))]:
 probe=cq.Workplane('XY').sphere(.4).translate(point).val()
 assert worlds[n].intersect(probe).Volume()<.001,(n,'raam niet open')
# De teruggebrachte kenmerken moeten werkelijk in de exportlijst staan.
names=set(worlds)
assert len([n for n in names if n.startswith('70_reling_')])>=38
assert len([n for n in names if n.startswith('71_trap_')])==8
assert len([n for n in names if n.startswith('72_helideknet_')])==5
assert len([n for n in names if n.startswith('32_vakwerk_')])==4
assert len([n for n in names if n.startswith('64_heli_ruit_')])==6
# Inzetruiten moeten vrij blijven van de witte omrandingen.
glass_checks=[]
for n in sorted(names):
 parent=None
 if n.startswith('19_ruitstrook_laag_'):parent='10_accommodatie_'+n.split('_')[-2]
 elif n=='19_ruitstrook_binnenhuis':parent='13_binnenhuis_galerij'
 elif n=='19_ruitstrook_voorhuis':parent='14_voorhuis'
 elif n.startswith('19_brugbeglazing_'):parent='17_brug'
 if parent:
  v=worlds[n].intersect(worlds[parent]).Volume()
  assert v<.03,(n,'inzetruit snijdt witte wand',v)
  glass_checks.append(dict(part=n,frame=parent,intersection_mm3=round(v,6)))
heli_body=worlds['60_heli_romp_BB'].fuse(worlds['60_heli_romp_SB'])
caps=[worlds[n] for n in names if n.startswith('64_heli_ruit_')]
for cap in caps:assert cap.intersect(heli_body).Volume()<.03
helicopter=cq.Compound.makeCompound([heli_body,*caps,worlds['61_heli_landingsgestel']])
b=helicopter.BoundingBox();assert b.zmax<=31.401 and b.ylen<=25.301
assert 213+b.xmin>176.2 and 213+b.xmax<295.35
assert 168.1+b.zmax<201.5
hangar_checks=[]
for y in [-32,32]:
 assert abs(y)+b.ylen/2<54.5
 positioned=helicopter.translate(cq.Vector(213,y,168.1))
 for q in D['parts']:
  if not (q['name'].startswith('75_') and q['name']!='75_dakkast'):continue
  for t in q['assembly_translations']:
   v=positioned.intersect(worlds[q['name']].translate(cq.Vector(*t))).Volume()
   assert v<.03,(y,q['name'],'heli raakt hangarinrichting',v)
   hangar_checks.append(dict(helicopter_y=y,obstacle=q['name'],intersection_mm3=round(v,6)))
# Het helidek heeft echte, passende uitsparingen voor H en gele cirkel.
for n in ['24_helidek_cirkel','24_helidek_H']:
 assert worlds[n].intersect(worlds['24_helidek']).Volume()<.03
# Systeembrede assemblage herimporteren: ieder solid geldig.
assy=cq.importers.importStep(str(R/'cad/step/ortelius-p2-assemblage.step')).solids().vals()
assert len(assy)>40 and all(s.isValid() for s in assy)
report=dict(status='PASS',revision='p2',unique_parts=len(results),assembly_solids=len(assy),checks=results,RC_hull_clearance=rc_collisions,glazing_clearance=glass_checks,hangar_clearance=hangar_checks,detail_features=D.get('details',{}),helicopter_headroom_mm=round(201.5-168.1-b.zmax,3),limitations='Statische geometriecontrole, geen fysieke print-, lek- of vaartest. Slicercontrole apart.')
(R/'print/controle.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
files=[p for d in ['cad/step','print/stl','print/3mf'] for p in sorted((R/d).glob('*')) if p.is_file()]
(R/'print/SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in files))
print('PASS',len(results),'onderdelen;',len(assy),'assemblagesolids')
