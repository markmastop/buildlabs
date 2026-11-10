"""Ortelius p2: parametrische CAD, millimeters, X naar boeg / Y bakboord / Z boven.
python cad/build.py; bestanden worden uitsluitend in dit project geschreven.
Vormbron: ../index.html v3. Constructiekeuzes staan in parameters.json.
"""
from pathlib import Path
import json, math, csv, zipfile
import xml.etree.ElementTree as ET
import cadquery as cq
import numpy as np
import trimesh
from details import masts, davits_cranes, enrich, helicopter_windows
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'cad/parameters.json').read_text())
W=P['hull_wall'];T=P['deck_wall'];H=P['house_wall'];G=P['fit_clearance']
STEP=R/'cad/step';STL=R/'print/stl';MF=R/'print/3mf'
for d in [STEP,STL,MF]:d.mkdir(parents=True,exist_ok=True)
records=[];objects={};assembly=cq.Assembly(name='Ortelius_p2')
NAVY='#163b70';WHITE='#eeeeea';GREEN='#477d60';BLACK='#242b30';ORANGE='#ed741e';YELLOW='#efce27'

def wp(s):return s if isinstance(s,cq.Workplane) else cq.Workplane(obj=s)
def box(dx,dy,dz,x=0,y=0,z=0):return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,False)).translate((x,y,z))
def poly(pts,z,h):return cq.Workplane('XY').polyline(pts).close().extrude(h).translate((0,0,z))
def wire(pts,z=0):return cq.Workplane('XY').polyline(pts).close().wire().val().translate(cq.Vector(0,0,z))
def offset(w,d):return w.offset2D(-d,kind='intersection')[0]
def prism(w,h):return cq.Workplane('XY').add(w).toPending().extrude(h)
def clip(s,a,b):return wp(s).intersect(box(b-a,600,600,(a+b)/2,0,-20))
def join(items):
 s=wp(items[0])
 for q in items[1:]:s=s.union(wp(q))
 return s.clean()
def rod(a,b,r):
 a=cq.Vector(*a);d=cq.Vector(*b)-a
 return cq.Workplane(obj=cq.Solid.makeCylinder(r,d.Length,a,d.normalized()))
def plan(a,b,hw,ac=4,fc=15):return [(a+ac,-hw),(b-fc,-hw),(b,-hw+fc),(b,hw-fc),(b-fc,hw),(a+ac,hw),(a,hw-ac),(a,-hw+ac)]
def loft(rings):return cq.Workplane(obj=cq.Solid.makeLoft([wire(pts,z) for z,pts in rings],ruled=True))
def hollow_plan(pts,z,h,th=H):
 w=wire(pts,z);return prism(w,h).cut(prism(offset(w,th),h+2).translate((0,0,-1)))
def yz_panel(pts,x,depth):return cq.Workplane('YZ',origin=(x,0,0)).polyline(pts).close().extrude(depth)
def xz_panel(pts,y,depth):return cq.Workplane('XZ',origin=(0,y,0)).polyline(pts).close().extrude(depth)

def write_3mf(mesh,path,name):
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
 root=ET.Element('{'+ns+'}model',unit='millimeter',attrib={'{http://www.w3.org/XML/1998/namespace}lang':'nl-NL'})
 ET.SubElement(root,'{'+ns+'}metadata',name='Title').text=name
 res=ET.SubElement(root,'{'+ns+'}resources');ob=ET.SubElement(res,'{'+ns+'}object',id='1',type='model',name=name)
 me=ET.SubElement(ob,'{'+ns+'}mesh');vs=ET.SubElement(me,'{'+ns+'}vertices');ts=ET.SubElement(me,'{'+ns+'}triangles')
 for v in mesh.vertices:ET.SubElement(vs,'{'+ns+'}vertex',**dict(zip(['x','y','z'],[f'{x:.6f}' for x in v])))
 for f in mesh.faces:ET.SubElement(ts,'{'+ns+'}triangle',**dict(zip(['v1','v2','v3'],map(str,f))))
 build=ET.SubElement(root,'{'+ns+'}build')
 xy=128-mesh.extents[:2]/2
 ET.SubElement(build,'{'+ns+'}item',objectid='1',transform=f'1 0 0 0 1 0 0 0 1 {xy[0]:.6f} {xy[1]:.6f} 0')
 data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
 if path.exists():
  with zipfile.ZipFile(path) as old:
   if old.read('3D/3dmodel.model')==data:return
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" Target="/3D/3dmodel.model"/></Relationships>')
  z.writestr('3D/3dmodel.model',data)

def add(name,shape,color=WHITE,qty=1,note='',rotate=None,include=True,placements=None,group='bovenbouw'):
 shape=wp(shape).clean();solids=shape.solids().vals()
 assert len(solids)==1 and solids[0].isValid(),(name,'geen enkel geldig solid',len(solids))
 s=solids[0];objects[name]=s
 out=shape
 if rotate:out=out.rotate((0,0,0),rotate[0],rotate[1])
 b=out.val().BoundingBox();shift=(-b.xmin,-b.ymin,-b.zmin);out=out.translate(shift)
 cq.exporters.export(out,str(STEP/(name+'.step')))
 cq.exporters.export(out,str(STL/(name+'.stl')),tolerance=.025,angularTolerance=.10)
 m=trimesh.load_mesh(STL/(name+'.stl'),process=True)
 # OCCT kan bij een bolpool een driehoek met nul oppervlak schrijven.
 # Alleen zulke degeneraties verwijderen; gaten of echte vormfouten niet repareren.
 keep=m.nondegenerate_faces(height=1e-8)
 if not keep.all():
  m.update_faces(keep);m.remove_unreferenced_vertices();m.export(STL/(name+'.stl'))
  m=trimesh.load_mesh(STL/(name+'.stl'),process=True)
 assert m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1,(name,'mesh-topologie')
 assert max(m.extents)<P['max_print_size']+.001,(name,'P2S-bouwvolume',m.extents)
 write_3mf(m,MF/(name+'.3mf'),name)
 poses=placements if placements is not None else [(0,0,0)]*qty
 if include:
  assert len(poses)==qty
  for i,p in enumerate(poses):
   assembly.add(s.translate(cq.Vector(*p)),name=name+'_'+str(i+1),color=cq.Color(color))
 rec=dict(name=name,quantity=qty,group=group,color=color,print_mm=np.round(m.extents,3).tolist(),volume_cm3=round(m.volume/1000,4),asa_solid_mass_g=round(m.volume/1000*P['asa_density_g_cm3']*qty,2),petg_solid_mass_g=round(m.volume/1000*P['petg_density_g_cm3']*qty,2),note=note,rotation=rotate,bed_translation=shift,assembly_translations=poses if include else [],included=include)
 records.append(rec);print(name,rec['print_mm'],'OK',flush=True)
 return shape

# Hoofdomtrekken volgen dezelfde taper als de goedgekeurde browser-vormstudie.
def station(z):
 ss=P['hull_stations']
 for a,b in zip(ss,ss[1:]):
  if z<=b[0]:
   t=max(0,(z-a[0])/(b[0]-a[0]));return [a[i]+t*(b[i]-a[i]) for i in range(1,4)]
 return ss[-1][1:]
def contour(z,fore=False):
 hw,a,b=station(z);start=240 if fore else a;ts=.58;ss=.055;sf=.78
 def width(x):
  t=(x-a)/(b-a);f=1
  if t>ts:f=math.sqrt(max(0,1-((t-ts)/(1-ts))**2))
  if t<ss:f*=sf+(1-sf)*math.sqrt(max(0,1-((ss-t)/ss)**2))
  return hw*f
 xs=np.linspace(start,b,P['hull_samples_per_side'])
 # De laatste twee vakken tot de steven fijner en sinusvormig verdelen: met gelijke stappen
 # werd de boeg een wig van circa 26 mm lang en 62 mm breed in plaats van een ronde steven.
 # Alle punten vóór xs[-3] blijven gelijk, dus de rompdelen 1-3 veranderen niet.
 xs=np.concatenate([xs[:-3],xs[-3]+(b-xs[-3])*np.sin(np.linspace(0,1,P['bow_tip_samples']+1)*math.pi/2)])
 return [(float(x),-width(x)) for x in xs[:-1]]+[(b,0)]+[(float(x),width(x)) for x in xs[-2::-1]]
def hull_solid(zs,inset=0,fore=False):
 wires=[wire(contour(z,fore),z) for z in zs]
 if inset:wires=[offset(w,inset) for w in wires]
 return cq.Workplane(obj=cq.Solid.makeLoft(wires,ruled=True))
print('Romp opbouwen...',flush=True)
low_z=[s[0] for s in P['hull_stations'] if s[0]<=107]
outer=hull_solid(low_z)
# Ook 3 mm verticaal verschuiven: horizontaal offset alleen geeft te dunne schuine kimmen.
inner=hull_solid(low_z,W).translate((0,0,W))
lower=outer.cut(inner)
upper=hull_solid([107,114,139],fore=True).cut(hull_solid([103,111,136,140],W,fore=True).translate((0,0,3)))
hull=lower.union(upper)
# Binnenrand: de afneembare voorste dekmodules rusten op een ingelijmde 5 mm lip.
w=wire(contour(136,True),133);ledge=prism(offset(w,1.5),3).cut(prism(offset(w,8.5),5).translate((0,0,-1)))
hull=hull.union(ledge)
# Achterschip met schroefopening: onder de toonbank (z 44-47) loopt de romp uit in een smalle
# scheg met de stevenbuis, zodat een schroef van Ø40 en een roer erachter vrij draaien.
# Vanaf x=212 is de buitenvorm exact gelijk aan de oorspronkelijke romp; rompdeel 1 sluit dus
# ongewijzigd aan op rompdeel 2 en de lasstrook.
ST=P['stern']
def interp(tab,z,cols):
 for a,b in zip(tab,tab[1:]):
  if z<=b[0]:
   t=max(0,(z-a[0])/(b[0]-a[0]));return [a[i]+t*(b[i]-a[i]) for i in cols]
 return [tab[-1][i] for i in cols]
def contour_aft(z,end=260):
 hw,a,b=station(z);ax,ahw,L=interp(ST['aft_stations'],z,[1,2,3]);sf=ahw/hw
 # Dichter bij het einde dichter bemonsteren: de afronding is daar het steilst.
 xs=[ax+L*(1-math.cos(u*math.pi/2)) for u in np.linspace(0,1,ST['aft_samples'])]+[end]
 def wd(x):
  u=x-ax
  if u>=L:return hw
  v=(L-u)/L;return hw*(sf+(1-sf)*math.sqrt(max(0,1-v*v)))
 return [(float(x),-wd(x)) for x in xs]+[(float(x),wd(x)) for x in xs[::-1]]
def convex_inset(pts,d):
 # Binnenoffset van een convexe contour: iedere zijde d naar binnen, hoekpunten als snijpunt
 # (verstek). Zijden die daarbij omklappen vallen weg. OCCT offset2D faalt op enkele van deze ringen.
 P=[np.array(q,float) for q in pts]
 while True:
  n=len(P);lines=[]
  for i in range(n):
   a,b=P[i],P[(i+1)%n];t=(b-a)/np.linalg.norm(b-a);nrm=np.array([-t[1],t[0]])
   lines.append((a+nrm*d,t))
  Q=[]
  for i in range(n):
   (p1,t1),(p2,t2)=lines[i-1],lines[i]
   den=t1[0]*t2[1]-t1[1]*t2[0]
   Q.append(p2 if abs(den)<1e-12 else p1+t1*(((p2-p1)[0]*t2[1]-(p2-p1)[1]*t2[0])/den))
  bad=[i for i in range(n) if np.dot(Q[(i+1)%n]-Q[i],P[(i+1)%n]-P[i])<=0]
  if not bad:return [tuple(q) for q in Q]
  del P[bad[0]+1 if bad[0]+1<n else 0]
def aft_solid(zs,inset=0):
 wires=[]
 for z in zs:
  r=contour_aft(z)
  if not inset:wires.append(wire(r,z));continue
  try:wires.append(offset(wire(r,z),inset))
  except ValueError:wires.append(wire(convex_inset(r,inset),z))  # zelfde resultaat, robuust
 return cq.Workplane(obj=cq.Solid.makeLoft(wires,ruled=True))
aft_z=ST['ring_heights']
aft_outer=aft_solid(aft_z)
aft_lower=aft_outer.cut(aft_solid(aft_z,W).translate((0,0,W)))
# Buitenkant is vanaf x=212 identiek; de binnenwand van de afgeronde lofts wijkt daar nog
# enkele tienden af. Daarom vanaf ST['join_x'] de oorspronkelijke wand gebruiken, zodat het
# snijvlak en de lasstrook bij x=227,5 precies blijven zoals ze waren.
aft_lower=clip(aft_lower,0,ST['join_x']).union(clip(lower,ST['join_x'],P['hull_cuts'][1]))
for i,(a,b) in enumerate(zip(P['hull_cuts'],P['hull_cuts'][1:])):
 add(f'01_romp_{i+1}',clip(aft_lower if i==0 else hull,a,b),NAVY,group='romp',rotate=((0,1,0),90 if i<3 else -90),note='Snijvlak op bed; buitenste overhangen controleren. Epoxy en glasband aan binnenzijde.')
# Losse interne lasstroken volgen de binnenvorm; 0,25 mm lijmspeling.
splice_outer=hull_solid(low_z,W+G).translate((0,0,W+G))
splice_inner=hull_solid(low_z,W+G+P['splice_wall']).translate((0,0,W+G+P['splice_wall']))
splice=splice_outer.cut(splice_inner).intersect(box(1100,400,103.75,450,0,0))
for i,x in enumerate(P['hull_cuts'][1:-1]):
 s=clip(splice,x-P['splice_length']/2,x+P['splice_length']/2)
 add(f'02_lasstrook_{i+1}',s,WHITE,group='romp',rotate=((0,1,0),90),note='24 mm breed; half in ieder rompdeel. Epoxylijmspeling 0,25 mm, niet klemmen.')
# Achterste vloer: 240 mm met aparte naden. Dekvoorstukken vallen binnen de rompwand.
aft_pts=plan(2,240,82,17,3)
aftdeck=poly(aft_pts,104,3).cut(box(150,126,6,145,0,103))
seat=box(162,138,3,145,0,101).cut(box(138,114,5,145,0,100))
aftdeck=aftdeck.union(seat)
lid=box(149.5,125.5,3,145,0,104)
for x in [85,205]:
 for y in [-60,60]:
  drill=cq.Workplane('XY').center(x,y).circle(1.6).extrude(9).translate((0,0,100))
  aftdeck=aftdeck.cut(drill);lid=lid.cut(drill)
add('03_werkdek_achter',aftdeck,GREEN,group='dek',note='Vast verlijmen; servo-/as-serviceluik met onderliggende oplegring.')
add('03_serviceluik_achter',lid,GREEN,group='dek',note='Afneembaar: 4 × M3 met eigen moeren; dunne afdichtingsband op oplegring.')
fore_deck=prism(offset(wire(contour(139,True),136),W+G),3)
for i,(a,b) in enumerate([(240,455),(455,682.5),(682.5,901)]):
 add(f'04_hoofddek_{i+1}',clip(fore_deck,a+G,b-G),GREEN,group='dek',note='Afneembare module op romp-lip; rand met schuimband afdichten, niet onderdompelbaar.')
# Losse lijmsteunen voor aftdek en promenade, M3 doorboring voor optionele borging.
block=box(12,8,10).cut(cq.Workplane('XY').circle(1.6).extrude(12))
add('05_deksteun_M3',block,WHITE,qty=16,include=False,group='montage',note='16 universele lijmsteunen. M3-moer/bout zelf toevoegen; pas bij proefmontage positioneren.')
add('05_deklijmstrip',box(60,12,2),WHITE,qty=8,include=False,group='montage',note='Voeg de drie hoofddekpanelen tot één afneembare unit; vier strips per naad onder het dek.')
# Doorlopende bakverschansing: eenvoudig maar fysiek gesloten geprint paneel.
bow_pts=contour(139,True)
# De bovenrand waaiert uit tot X=910 mm, overeenkomstig de totale modellengte.
# Zeeg zoals in de vormstudie: 11 mm hoog tot X=740, oplopend naar 15,5 mm aan de steven.
BW_TOP=16.5
def sheer(x):return 11+4.5*min(1.1,max(0,(x-740)/160))**2
bow_top=[(x+10*BW_TOP/15.5*(max(0,x-800)/100)**2,y*(1+.025*BW_TOP/15.5*(max(0,x-800)/100)**2)) for x,y in bow_pts]
bowring=loft([(139,bow_pts),(139+BW_TOP,bow_top)])
inner_bow=cq.Workplane(obj=cq.Solid.makeLoft([offset(wire(bow_pts,138.9),1.6),offset(wire(bow_top,139.1+BW_TOP),1.6)],ruled=True))
sheer_cut=xz_panel([(700,139+sheer(700))]+[(float(x),139+sheer(float(x))) for x in np.linspace(740,916,23)]+[(916,170),(700,170)],150,300)
bowring=clip(bowring.cut(inner_bow).cut(sheer_cut),716,912)
add('06_bakverschansing',bowring,WHITE,note='Buitenrand op bestaande romp; met zeeg (11 naar 15,5 mm) en ronde steven volgens de vormstudie.')
# Lagere accommodatie: open onder- en bovenzijde; raamopeningen echt uitgesneden.
lowpts=plan(175,714,82,4,30);house=hollow_plan(lowpts,139,27)
for sd,xs in [(-1,[192,221,254,280,312,341,372,421.1,428.9,467.1,474.9,510.1,517.9,556.1,563.9,600.1,607.9,647.1,654.9,692]),(1,[194,223,253,284,313,342,376,424.1,431.9,469.1,476.9,513.1,520.9,556.1,563.9,603.1,610.9,648.1,655.9,692])]:
 for x in xs:house=house.cut(box(2.5,32,5.3,x,sd*78,148.65))
for y in [-40,-31,-8,1,32,41]:house=house.cut(box(7,2.5,5.3,713.5,y,148.65))
for x in [355,535]:house=house.union(box(4,162,2,x,0,139))
for i,(a,b) in enumerate([(175,355),(355,535),(535,714)]):add(f'10_accommodatie_{i+1}',clip(house,a,b),note='Raamgaten; donker schilderen of transparante folie achterlijmen.')
# Dak achter lage accommodatie; bovenbouw op het dek maken en per module afnemen.
add('11_dak_lage_accommodatie',poly(plan(298,412,80,2,3),164,2),GREEN,group='dek')
boatdeck=poly(plan(412,716,82.5,3,25),164,2.9)
for i,(a,b) in enumerate([(412,560),(560,716)]):add(f'12_sloependek_{i+1}',clip(boatdeck,a,b),GREEN,group='dek')
innerhouse=hollow_plan(plan(420,608,46.5,3.5,3.5),166.9,26.1)
for sd in [-1,1]:
 for x in [440,502,567]:innerhouse=innerhouse.cut(box(15.5,15,10,x,sd*46,175.8))
add('13_binnenhuis_galerij',innerhouse)
frontpts=plan(605,698,67,4,22);front=hollow_plan(frontpts,166.9,26.1)
for sd in [-1,1]:
 for x in [624,634,658,670]:front=front.cut(box(3.4,12,6.1,x,sd*66,177.35))
add('14_voorhuis',front)
gallery_roof=[[412,-80.5],[605,-80.5],[605,-70.5],[681,-70.5],[702,-49.5],[702,49.5],[681,70.5],[605,70.5],[605,80.5],[412,80.5]]
for i,(a,b) in enumerate([(412,560),(560,702)]):add(f'15_galerijdak_{i+1}',clip(poly(gallery_roof,191,3.1),a,b),GREEN,group='dek')
openings=[[(422.5,172.4),(462.5,172.4),(470.5,190.4),(430.5,190.4)],[(480,172.4),(523.5,172.4),(531.5,190.4),(488,190.4)],[(541,172.4),(591.5,172.4),(600.5,190.4),(550,190.4)]]
for sd in [-1,1]:
 gal=box(198,2.2,24.1,513,sd*78,166.9)
 for pts in openings:gal=gal.cut(xz_panel(pts,sd*78+4,8))
 add('16_galerijwand_'+('BB' if sd>0 else 'SB'),gal)
# Brug: 11 frontramen; aansluitend smaller dekhuis en losse kap.
bridge=join([hollow_plan(plan(641,696,80,5,5),194.1,28.9),hollow_plan(plan(585,643,60,4,3),194.1,28.9)])
# De overlappende binnenwand bij x641 verwijderen voor één samenhangende cabine.
bridge=bridge.cut(box(4,112,30,642,0,193.5))
for y in np.linspace(-70,70,11):bridge=bridge.cut(box(14,11.4,11,695,y,207.5))
for sd in [-1,1]:
 for x in [652,667,682]:bridge=bridge.cut(box(11.4,10,11,x,sd*79,207.5))
 for x in [595,610,625]:bridge=bridge.cut(box(10,10,8.5,x,sd*60,208.5))
add('17_brug',bridge)
roof=join([poly(plan(639,699,82.5,5,6),223,3),poly(plan(583,642,62,4,3),223,3)])
add('18_brugdak',roof,GREEN,group='dek')
# Promenadedek en helidek, met afzonderlijke steunen (volle volumes geen browservlakken).
add('20_promenadedek',poly(plan(2,242,87,16.5,4),136,3),GREEN,group='dek')
post=box(2.4,2.5,29.0)
poses=[(x,sd*y,107) for x,y in [(19,73),(72,81),(126,81),(164,81)] for sd in [-1,1]]
add('21_kolom_onder',post,qty=8,placements=poses)
poses2=[(x,sd*y,139) for x,y in [(19,73),(72,81),(126,81),(164,81)] for sd in [-1,1]]
add('22_kolom_helidek',box(2.4,2.5,23.5),qty=8,placements=poses2)
# Terugliggende ramenwand onder achterdek.
# 29 hoog: sluit aan op de onderzijde van het promenadedek (was 25, met 4 mm open kier).
cab=hollow_plan(plan(100,237,73,2,2),107,29)
for sd in [-1,1]:
 for x in [114,138,172,196,220]:cab=cab.cut(box(8,8,6,x,sd*73,122.5))
add('23_achterkajuit',cab)
helideck=poly(plan(0,175,89,18,10),162.5,5)
ring=cq.Workplane('XY').center(87,0).circle(56).circle(50.5).extrude(.9).translate((0,0,166.6))
ringcut=cq.Workplane('XY').center(87,0).circle(56.15).circle(50.35).extrude(1.2).translate((0,0,166.5))
letterH=join([box(37,5,.9,87,-13.5,166.6),box(37,5,.9,87,13.5,166.6),box(5,31,.9,87,0,166.6)])
hcut=join([box(37.3,5.3,1.2,87,-13.5,166.5),box(37.3,5.3,1.2,87,13.5,166.5),box(5.3,31.3,1.2,87,0,166.5)])
add('24_helidek',helideck.cut(ringcut).cut(hcut),GREEN,group='dek',note='Met uitsparingen voor gele cirkel en witte H; inzetstukken circa 0,15 mm lijmspeling.')
add('24_helidek_cirkel',ring,YELLOW,group='dek')
add('24_helidek_H',letterH,WHITE,group='dek')
# Hangar: ingang exact 124 breed / 201,5 hoog, met hoeken zoals browsermodel.
hg=join([box(123,2.3,38.1,236.5,sd*78.8,166.9) for sd in [-1,1]]+[box(2.3,158,38.1,296.5,0,166.9)])
front=box(2.4,160,38.1,175,0,166.9)
opening=[(-62,168.1),(62,168.1),(62,194.7),(54.5,201.5),(-54.5,201.5),(-62,194.7)]
front=front.cut(yz_panel(opening,172,6));hg=hg.union(front)
add('25_hangarwanden',hg,note='Dunne ramenfolie niet nodig. Schilder binnenwanden vóór dakmontage.')
add('26_hangarvloer',box(120.6,155.3,2.1,236.5,0,166),GREEN,group='dek')
add('27_hangardak',poly([[173,-82],[300,-82],[300,-64],[370,-64],[370,64],[300,64],[300,82],[173,82]],205,2),GREEN,group='dek')
add('28_hangar_voorhuis',hollow_plan(plan(298,365,59,2,4),166.9,38.1))
# Schoorsteen: holle mantel, schuine zwarte kap.
funnel=loft([(207,plan(264,330,28,3.5,6.5)),(252,plan(266,336,24.5,3,6))])
funnel=funnel.cut(loft([(206,plan(266,328,26,3,6)),(253,plan(268,334,22.5,3,5))]))
add('30_schoorsteen',funnel)
cap=xz_panel([(250,260),(344,255),(342,251),(254,251)],29.5,59)
add('31_schoorsteenkap',cap,BLACK)
# Ruimtelijke mast en gedetailleerde radarinstallatie uit de vormstudie.
masts(globals())
# Voormast volgens de vormstudie: taps (Ø5,2 naar Ø3,2), ra dwarsscheeps op 248, toplicht op 271.
# De kraag op 262 houdt de stagen van garen op hun plaats; de voet geeft lijmvlak op het bakdek.
foremast=cq.Workplane(obj=cq.Solid.makeCone(2.6,1.6,131,cq.Vector(806,0,139),cq.Vector(0,0,1)))
foremast=join([foremast,rod((806,0,139),(806,0,140.6),4.5),rod((806,0,261.3),(806,0,262.7),3.3),
 box(1.8,32,1.8,806,0,247.1),cq.Workplane('XY').sphere(2.1).translate((806,0,271))])
add('34_voormast',foremast,WHITE,rotate=((0,1,0),90),note='Liggend printen, ra vlak op het bed. Stagen van dun garen boven de kraag vastknopen en naar de verschansing spannen.')
# Dekuitrusting: twee sloepen (maat/kleur browser), davits, kranen, lichtkap en banken.
# Twee bokken per sloep tegen de zijwand van de accommodatie, buiten de reling om.
# Vervangt het platform van 94 x 32 mm dat 6,6 mm boven het dek zweefde en de reling doorsneed.
for sd,label in [(1,'BB'),(-1,'SB')]:
 chock=yz_panel([(sd*82,156),(sd*84.5,156),(sd*84.5,162),(sd*97,173.5),(sd*101,173.5),(sd*101,176.5),(sd*82,176.5)],-2,4)
 add('39_sloepbok_'+label,chock,WHITE,qty=2,placements=[(326,0,0),(360,0,0)],rotate=((0,1,0),90),note='Console onder de sloep; vlak tegen de accommodatiewand lijmen, boven de raamrij en buiten de reling.')
boat=loft([(0,plan(-35,36,9,6,8)),(12,plan(-42,43,14.2,8,12)),(26,plan(-30,29,8.3,6,6.5))])
add('40_reddingsboot',boat,ORANGE,qty=2,placements=[(346,-89,176.5),(346,89,176.5)],note='Ramen zwart schilderen; rust op twee bokken 39 per zijde.')
davits_cranes(globals())
skylight=loft([(194.1,plan(492,550,30,1,1)),(198,plan(492,550,30,1,1)),(204.4,plan(492,550,1,0.5,0.5))])
add('43_lichtkap',skylight,'#62939a',note='Glasvlakken schilderen; solide detail om vlakke browserruiten printbaar te maken.')
bench=join([box(38,10,2,0,0,6),box(38,2,9,0,5,8),box(3,10,6,-14,0,0),box(3,10,6,14,0,0)])
for y in [-2,2]:bench=bench.cut(box(37,.8,2.2,0,y,6))
add('44_bank',bench,'#8a6944',qty=2,placements=[(521,-45.5,194.1),(521,45.5,194.1)])
# Losse relingpanelen kunnen plat geprint en op maat geknipt worden.
rail=join([box(100,1.2,1.2,50,0,z) for z in [3,7,11]]+[box(1.4,1.2,12,x,0,0) for x in [0,20,40,60,80,100]])
add('45_reling_100mm',rail,WHITE,qty=2,include=False,rotate=((1,0,0),90),note='Twee reservestroken; de juiste relingen staan als eigen delen in de CAD-assemblage.')
# Verstelbare RC-inbouw: houders, geen geprinte motoren/accu's of schroefassen.
tray=box(160,68,3,460,0,15)
tray=join([tray,box(160,3,9,460,-32.5,18),box(160,3,9,460,32.5,18),box(3,62,9,381.5,0,18),box(3,62,9,538.5,0,18)])
for x in [405,515]:
 for sd in [-1,1]:tray=tray.cut(box(14,8,5,x,sd*26,14))
add('50_accubak_2S',tray,BLACK,group='RC',note='Binnenruimte 154 × 62 mm; klittenband door sleuven, montagevoet op maat uitvullen.')
motorplate=box(116,78,4,300,0,16)
for y in [-26,26]:motorplate=motorplate.cut(box(80,3.4,8,300,y,14))
add('51_motorplaat_verstelbaar',motorplate,BLACK,group='RC',note='Voor metalen motorbeugel; M3-sleuven. Motortype, ashoogte en uitlijning eerst vastleggen.')
# Verder naar voren en hoger dan in p2: de smallere afloop laat bij x=110 te weinig breedte.
SV=ST['servo_plate'];sx,sy,sz=SV
servotray=box(56,36,3,sx,sy,sz).cut(box(41,21,6,sx,sy,sz-1))
for x in [sx-24,sx+24]:servotray=servotray.cut(cq.Workplane('XY').center(x,sy).circle(1.6).extrude(7).translate((0,0,sz-2)))
add('52_servoplaat',servotray,BLACK,group='RC',note='Proefmaat 41 × 21 mm opening, M3-hartafstand 48 mm; aanpassen aan werkelijke servo.')
plate=box(65,42,3)
for x in [-24,24]:
 for y in [-14,14]:plate=plate.cut(cq.Workplane('XY').center(x,y).circle(1.6).extrude(5))
add('53_elektronicaplaat',plate,BLACK,qty=3,placements=[(370,43,30),(555,0,25),(670,-20,30)],group='RC',note='Voor regelaar/ontvanger met klittenband; neutrale M3-plaat.')
ballast=box(55,45,12).cut(box(50,40,15,0,0,2.5))
add('54_ballastbak',ballast,BLACK,qty=2,placements=[(575,0,15),(635,0,15)],group='RC')
# Tunnel als afzonderlijke proefbuis. Gesloten romp blijft dicht tot de echte hardware gekozen is.
tunnel=cq.Workplane('XY').circle(P['tunnel_outside_diameter']/2).circle(P['tunnel_inside_diameter']/2).extrude(125)
add('55_boegschroef_proeftunnel',tunnel,BLACK,include=False,group='RC',note='Alleen maattest ID20/OD23 ×125; geen functionele boegschroef, geen gaten in romp.')
# Rudder and metal-stock socket: no printed rotating shafts.
# Gebalanceerd hangroer achter de schroef: profiel NACA 00xx, voorrand naar de schroef,
# roerkoning op circa 27% van de koorde. Open achterrand 0,8 mm voor FDM.
RD=ST['rudder'];le,c,th=RD['leading_edge_x'],RD['chord'],RD['thickness_ratio']
def naca(xi):return 5*th*c*(.2969*math.sqrt(xi)-.1260*xi-.3516*xi**2+.2843*xi**3-.1036*xi**4)
xi=[(1-math.cos(u*math.pi))/2 for u in np.linspace(0,1,40)]
half=[max(naca(q),.4) if q>0 else 0 for q in xi]
prof=[(le-q*c,h) for q,h in zip(xi,half)]+[(le-q*c,-h) for q,h in zip(xi[::-1],half[::-1])][1:-1]
rudder=cq.Workplane('XY').polyline(prof).close().extrude(RD['top_z']-RD['bottom_z']).translate((0,0,RD['bottom_z']))
rudder=rudder.cut(cq.Workplane('XY').center(RD['stock_x'],0).circle((P['rudder_stock_diameter']+.2)/2).extrude(60))
add('56_roerblad',rudder,NAVY,group='RC',note='Staand printen, voet op het bed. Metalen roeras Ø4 met epoxy verlijmen; roerkoker van de toonbank tot boven de waterlijn uit handelsdelen.')
# Schroefmal: omhullende van een Ø40 schroef (6 mm diep), als maatcontrole op de echte romp.
PR=ST['propeller'];hx,hz=PR['hub_x'],PR['hub_z']
gauge=cq.Workplane('YZ',origin=(hx-PR['sweep_depth']/2,0,0)).center(0,hz).circle(PR['diameter']/2).circle(2.1).extrude(PR['sweep_depth'])
add('57_schroefmal_40',gauge,'#b8873a',group='RC',rotate=((0,1,0),90),note='Geen schroef: mal van de schroefcirkel Ø40 × 6. Op de as schuiven en controleren dat er rondom circa 4 mm speling naar de romp is.')
# Twee helikopters. Romp in twee vlak printbare helften, losse skids en rotors.
secs=[(-33.35,13.5,.8,1),(-30,14.2,6,6.2),(-22,15.2,8.8,10),(-10,15.5,9,10.85),(6,15.8,7.8,9.1),(17,17.5,5.2,5.9),(25,19,2.8,3.2)]
wires=[]
for x,z,rz,ry in secs:
 wires.append(cq.Workplane('YZ',origin=(x,0,z)).ellipse(ry,rz).wire().val())
heli=cq.Workplane(obj=cq.Solid.makeLoft(wires,ruled=True))
heli=heli.union(rod((16,0,19),(69,0,20.5),2.5))
heli=heli.union(xz_panel([(63,18.5),(75.95,18.5),(73,30.5),(69,30.5)],.8,1.6))
heli=heli.union(box(7.2,25.3,1.2,58,0,18.2))
heli=heli.union(cq.Workplane('XY').ellipse(10.5,5.5).extrude(5).translate((7,0,23.3)))
heli=heli.union(rod((0,0,24),(0,0,30.9),1.1)).union(cq.Workplane('XY').circle(2.2).extrude(1).translate((0,0,30.4)))
# Echte cockpitopeningen met afzonderlijke, gebogen donkergekleurde ruiten.
heli,heli_glazing=helicopter_windows(heli,secs)
for name,cap in heli_glazing:
 add(name,cap,'#163a49',qty=2,include=False,group='heli',note='Gebogen inzetruit, circa 1 mm dik; rondom 0,12–0,15 mm lijmspeling. Ook als schildermal te gebruiken.')
# Skid sleeves via butt surfaces, no blind hidden press fits.
for sd in [-1,1]:
 half=heli.intersect(box(140,35,60,20,sd*17.5,-1))
 add('60_heli_romp_'+('BB' if sd>0 else 'SB'),half,YELLOW,qty=2,include=False,rotate=((1,0,0),90 if sd>0 else -90),group='heli',note='Twee exemplaren per zijde; middenvlak op bed, vlak verlijmen. Losse ruiten 64 in de uitgespaarde cockpit lijmen.')
skids=[]
for sd in [-1,1]:
 skids+=[rod((-28.5,sd*11.2,0.9),(19,sd*11.2,.9),.9),rod((-28.5,sd*11.2,.9),(-30.2,sd*11.2,3.4),.8)]
 for x in [-18.5,8]:skids.append(rod((x,sd*11.2,1.2),(x,sd*6.5,9.3),.8))
skids+=[rod((-18.5,-6.5,9),(-18.5,6.5,9),.9),rod((8,-6.5,9),(8,6.5,9),.9)]
# Crosspieces connect upper legs; all surfaces overlap, thus one printable solid.
skid=join(skids)
add('61_heli_landingsgestel',skid,BLACK,qty=2,include=False,group='heli',note='0,8–0,9 mm radius; geprint vanaf rails met steun onder dwarsbalkjes.')
blade=box(51,2.3,1.2,27.95,0,30.3)
add('62_heli_rotorblad',blade,BLACK,qty=6,include=False,group='heli',note='Drie per heli, lijmen op hub op 120 graden; voor hangar loslaten. 1,2 mm dik voor FDM.')
tail=join([box(1.2,1.2,18.6,0,0,0),box(18.6,1.2,1.2,0,0,8.7)])
add('63_heli_staartrotor',tail,BLACK,qty=2,include=False,rotate=((1,0,0),90),group='heli')
# Digitale assemblage toont beide geschaalde, gestalde toestellen; printhelften blijven los.
for i,y in enumerate([-32,32]):
 pos=cq.Vector(213,y,168.1)
 assembly.add(heli.translate(pos),name='heli_assemblage_'+str(i),color=cq.Color(YELLOW))
 assembly.add(skid.translate(pos),name='skids_assemblage_'+str(i),color=cq.Color(BLACK))
 for name,cap in heli_glazing:assembly.add(cap.translate(pos),name=name+'_'+str(i),color=cq.Color('#163a49'))
 assembly.add(tail.translate(cq.Vector(279.65,y+2.5,179.1)),name='heli_staartrotor_'+str(i),color=cq.Color(BLACK))
# Kleine passingstest: echte romp/lijmnaad op middenstation, als twee delen exporteren.
coupon=clip(hull,445,465).intersect(box(30,22,40,455,78,50))
for label,a,b in [('A',445,455),('B',455,465)]:
 add('00_pasproef_'+label,clip(coupon,a,b),NAVY,include=False,group='proef',rotate=((0,1,0),90),note='Eerst printen. Controleer las en lijmspeling vóór de vier grote rompdelen.')
add('00_pasproef_las',clip(splice,447,463).intersect(box(30,22,40,455,78,50)),WHITE,include=False,group='proef',rotate=((0,1,0),90))
# Herstel de zichtbare details als daadwerkelijke printonderdelen.
enrich(globals())
# De zes losse bladen worden in de CAD-stallingsstand in hun rekken getoond.
for y in [-69,69]:
 for k in range(3):assembly.add(blade.translate(cq.Vector(196.05,y,139.4+k*1.2)),name='opgeborgen_rotor_'+str(y)+'_'+str(k),color=cq.Color(BLACK))
# Uitvoer, rapport, massa en modeldata voor de losse CAD-viewer.
assembly.export(str(STEP/'ortelius-p2-assemblage.step'))
# Verouderde eigen exports horen niet tussen de actuele printdelen. P1 blijft in Git/het eerdere ZIP.
expected={q['name'] for q in records}
for folder,ext in [(STEP,'.step'),(STL,'.stl'),(MF,'.3mf')]:
 for f in folder.glob('*'+ext):
  if f.stem not in expected and f.name!='ortelius-p2-assemblage.step':f.unlink()
# OCCT schrijft spaties aan regeleinden; normaliseer de tekstexports voor Git.
for f in STEP.glob('*.step'):
 f.write_text('\n'.join(line.rstrip() for line in f.read_text().splitlines())+'\n')
report=dict(revision='p2',units='mm',scale=100,printer='Bambu Lab P2S 256³; modelmarge 5 mm per zijde',parts=records,unique_parts=len(records),print_quantity=sum(q['quantity'] for q in records),maximum_part_dimension_mm=max(max(q['print_mm']) for q in records),solid_ASA_mass_g=round(sum(q['asa_solid_mass_g'] for q in records),1),material='PETG',solid_PETG_mass_g=round(sum(q['petg_solid_mass_g'] for q in records),1),limitations=['Fotogebaseerde onderwatervorm','Geen fysieke pas-/water-/vaartest','RC-hardware niet gekozen; doorvoeren niet geboord','Slicerprofielen en ondersteuning apart controleren'])
report['details']=detail_report
outer_now=clip(aft_outer,0,227.5).union(clip(outer,227.5,900))
def buoy(z):
 v=outer_now.intersect(box(1100,300,z,450,0,0)).val();return dict(waterline_mm=z,displacement_freshwater_kg=round(v.Volume()/1e6,3),centre_of_buoyancy_x_mm=round(v.Center().x,1))
report['hydrostatics']=[buoy(z) for z in [44,54,64]]
(R/'print/onderdelen.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
with (R/'print/onderdelen.csv').open('w') as f:
 writer=csv.writer(f,lineterminator="\n");writer.writerow(['onderdeel','aantal','groep','X_mm','Y_mm','Z_mm','volledig_solide_ASA_g','volledig_solide_PETG_g','opmerking'])
 for q in records:writer.writerow([q['name'],q['quantity'],q['group'],*q['print_mm'],q['asa_solid_mass_g'],q['petg_solid_mass_g'],q['note']])
# De viewer gebruikt dezelfde meshes als de printbestanden.
from viewer import create_viewer
create_viewer(R,records)
print('GEREED',report['unique_parts'],'unieke delen,',report['print_quantity'],'prints',flush=True)
