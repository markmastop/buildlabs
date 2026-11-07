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
 if q['group']!='RC' or not q['included'] or q['name']=='56_roerblad':continue
 for p in q['assembly_translations']:
  s=worlds[q['name']].translate(cq.Vector(*p));v=sum(s.intersect(h).Volume() for h in hull)
  assert v<.1,(q['name'],p,'RC raakt romp',v)
  rc_collisions.append(dict(part=q['name'],translation=p,intersection_mm3=round(v,6)))
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
# Hangaropening en de helikoptermaxima (uit bronvorm, niet opgeruimde printoriëntatie).
helicopter=worlds['60_heli_romp_BB'].fuse(worlds['60_heli_romp_SB'])
b=helicopter.BoundingBox();assert b.zmax<=31.401 and b.ylen<=25.301
assert 213+b.xmin>176.2 and 213+b.xmax<295.35
assert 168.1+b.zmax<201.5
for y in [-32,32]:assert abs(y)+b.ylen/2<54.5
# Systeembrede assemblage herimporteren: ieder solid geldig.
assy=cq.importers.importStep(str(R/'cad/step/ortelius-p1-assemblage.step')).solids().vals()
assert len(assy)>40 and all(s.isValid() for s in assy)
report=dict(status='PASS',revision='p1',unique_parts=len(results),assembly_solids=len(assy),checks=results,RC_hull_clearance=rc_collisions,helicopter_headroom_mm=round(201.5-168.1-b.zmax,3),limitations='Statische geometriecontrole, geen fysieke print-, lek- of vaartest. Slicercontrole apart.')
(R/'print/controle.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
files=[p for d in ['cad/step','print/stl','print/3mf'] for p in sorted((R/d).glob('*')) if p.is_file()]
(R/'print/SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in files))
print('PASS',len(results),'onderdelen;',len(assy),'assemblagesolids')
