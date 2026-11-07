"""Smit-Lloyd 109 v4: photo-detail prototype; all dimensions in millimetres.
Original plans remain unavailable. These are engineering choices, not scale measurements.
CadQuery 2.8, trimesh, numpy, fonttools. Run from any directory.
"""
from pathlib import Path
import json,csv,math
import cadquery as cq
import trimesh
from smit_logo import add_logo

ROOT=Path(__file__).resolve().parents[1]
for folder in ['STL','STEP']:(ROOT/folder).mkdir(exist_ok=True)
OLD=cq.importers.importStep(str(ROOT/'inputs/SL109_v1_assemblage.step')).solids().vals()
P=json.loads((ROOT/'CAD/parameters.json').read_text())
parts=[];records=[];objects={}

def box(dx,dy,dz,x=0,y=0,z=0):
    return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,False)).translate((x,y,z))
def poly(pts,h,z=0):return cq.Workplane('XY').polyline(pts).close().extrude(h).translate((0,0,z))
def rounded(dx,dy,h,x=0,y=0,z=0,r=1):return box(dx,dy,h,x,y,z).edges('|Z').fillet(r)
def fore(length,width,h,z=0,inset=0):
    x=3+inset;yy=width/2;r=23-inset
    return (cq.Workplane('XY').moveTo(x+r,-yy).lineTo(length,-yy).lineTo(length,yy).lineTo(x+r,yy)
      .radiusArc((x,yy-r),-r).lineTo(x,-yy+r).radiusArc((x+r,-yy),-r).close().extrude(h).translate((0,0,z)))
def wire(pts,z=0):return cq.Workplane('XY').polyline(pts).close().wire().val().translate(cq.Vector(0,0,z))
def inset_wire(pts,offset,z):return cq.Workplane('XY').polyline(pts).close().offset2D(-offset).val().translate(cq.Vector(0,0,z))
def fore_wire(length,width,z,inset=0):return fore(length,width,1,z,inset).faces('<Z').wires().val()
def rwire(dx,dy,r,x,y,z):return rounded(dx,dy,1,x,y,z,r).faces('<Z').wires().val()
def on_plane(shape,plane):return cq.Workplane(obj=shape.val().transformShape(plane.rG))
def panel(w,h,plane,depth=.6,outline=False):
    out=rounded(w,h,depth,0,0,-.12,min(1,w/8))
    if outline:out=out.cut(rounded(w-1.6,h-1.6,depth+2,0,0,-1,min(.5,w/12)))
    return on_plane(out,plane)

def add(name,shape,*,roof=False,rotate=False,qty=1,note='',include=True,print_shape=None):
    if isinstance(shape,cq.Shape):shape=cq.Workplane(obj=shape)
    shape=shape.clean()
    assert shape.val().isValid(),(name,'BRep invalid')
    assert len(shape.solids().vals())==1,(name,'must be one solid')
    objects[name]=shape
    printable=shape if print_shape is None else print_shape
    printable=printable.rotate((0,0,0),(1,0,0),180) if rotate else printable
    b=printable.val().BoundingBox();printable=printable.translate((-b.xmin,-b.ymin,-b.zmin))
    stl=ROOT/'STL'/(name+'.stl');step=ROOT/'STEP'/(name+'.step')
    cq.exporters.export(printable,str(stl),tolerance=.03,angularTolerance=.12)
    cq.exporters.export(printable,str(step))
    m=trimesh.load_mesh(stl,process=True)
    assert m.is_watertight and m.is_winding_consistent and m.volume>0,(name,'invalid STL')
    assert len(m.split())==1,(name,'disconnected STL')
    assert m.extents[0]<=246 and m.extents[1]<=246,(name,'bed footprint')
    records.append(dict(part=name,qty=qty,print_mm=m.extents.round(3).tolist(),volume_cm3=round(m.volume/1000,3),
       one_solid=True,watertight=True,orientation='bovenzijde op bed' if rotate else 'onderzijde op bed',note=note))
    if include:parts.append((name,shape.val(),roof))
    print(name,'OK',m.extents.round(2),flush=True)
    return shape

# The original fit interface is deliberately preserved.
def ring(wall):
    a=box(204,152,6,160,0,-8).cut(box(204-2*wall,152-2*wall,8,160,0,-9))
    return a.union(box(212,160,2,160,0,-2).cut(box(204-2*wall,152-2*wall,4,160,0,-3)))
add('00_pasproef',ring(2),rotate=True,include=False,note='Eerst passen in 205 x 153 mm opening; 6 mm insteek.')
add('01_pasframe',cq.Workplane(obj=OLD[0]),rotate=True)
for i,name in [(1,'02_basis_voor'),(2,'03_basis_achter_bakboord'),(3,'03_basis_achter_stuurboord')]:add(name,OLD[i])
base=cq.Workplane(obj=OLD[1]).union(cq.Workplane(obj=OLD[2])).union(cq.Workplane(obj=OLD[3]))

# Lower house with recessed and chamfered rear bulkhead.
notch_pts=[(185,-36),(205,-52.5),(212,-52.5),(212,52.5),(205,52.5),(185,36)]
main_outer=fore(205,200,42,3).cut(poly(notch_pts,46,1))
iw=main_outer.faces('<Z').val().outerWire()
cavity=cq.Workplane('XY').add(iw).toPending().offset2D(-2).extrude(44).translate((0,0,-1))
main=main_outer.cut(cavity)
for x in [40,94,122,166]:
    for sign in [-1,1]:main=main.cut(box(9,12,11,x,sign*100,17))
for y in [0,23]:main=main.cut(box(10,9,9,185,y,26))
door_plane=cq.Plane(origin=(185,-23,22),xDir=(0,1,0),normal=(1,0,0))
main=main.union(panel(13,32,door_plane)).union(panel(13,32,door_plane,1.0,True))
porthole=cq.Workplane('YZ').center(-23,31).circle(2.5).extrude(8).translate((181,0,0))
main=main.cut(porthole).union(box(.9,2.8,1,185.25,-19,18))
add('04_dekhuis_met_achterdeur',main)

for sign,label,deck_i in [(1,'bakboord',6),(-1,'stuurboord',8)]:
    wing=rounded(115,50,42,262.5,sign*77.5,3,4).cut(rounded(111,46,44,262.5,sign*77.5,2,2))
    for x in [215,240]:wing=wing.cut(box(9,8,11,x,sign*102.5,17))
    add('05_vleugel_'+label,wing)
    add('06_vleugeldek_'+label,OLD[deck_i])

# Sloping rear transition. Rear deck and upper shell are one printable module.
slope=20/23
uo=cq.Solid.makeLoft([fore_wire(185,200,45),fore_wire(165,200,68)],ruled=True)
ui=cq.Solid.makeLoft([fore_wire(185+slope-2*math.sqrt(1+slope*slope),196,44,2),
                     fore_wire(165-slope-2*math.sqrt(1+slope*slope),196,69,2)],ruled=True)
upper=cq.Workplane(obj=uo.cut(ui))
for x in [40,115]:
    for sign in [-1,1]:upper=upper.cut(box(29,14,12,x,sign*100,51))
lower_roof=fore(205,200,3,45).cut(poly(notch_pts,7,44)).cut(cq.Workplane(obj=uo))
upper=upper.union(lower_roof)
add('07_bovendekhuis_met_achterdek',upper,note='Rechtop; zijraambruggen van 29 mm in slicer controleren.')
add('08_brugdek',OLD[11])

# Bridge: tilted forward window band, rounded window corners and door frames.
bottom=[(33,-48),(48,-68),(135,-68),(145,-58),(145,58),(135,68),(48,68),(33,48)]
top=[(25,-48),(45,-68),(135,-68),(145,-58),(145,58),(135,68),(45,68),(25,48)]
bo=cq.Solid.makeLoft([wire(bottom,71),wire(bottom,85),wire(top,113)],ruled=True)
bi=cq.Solid.makeLoft([inset_wire(bottom,2,70),inset_wire(bottom,2,85),inset_wire(top,2,114)],ruled=True)
bridge=cq.Workplane(obj=bo.cut(bi))
mid=[(a[0]*.6+b[0]*.4,a[1]*.6+b[1]*.4) for a,b in zip(bottom,top)]
for a,b in zip(mid,mid[1:]+mid[:1]):
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);n=max(1,int(length/21));w=min(16,(length-(n+1)*4)/n)
    for i in range(n):
        f=(i+.5)/n
        cutter=box(w,22,22,z=85).edges('|Y').fillet(.9).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(dy,dx))).translate((a[0]+dx*f,a[1]+dy*f,0))
        bridge=bridge.cut(cutter)
for y in [-23.2,0,23.2]:
    plane=cq.Plane(origin=(145,y,92.75),xDir=(0,1,0),normal=(1,0,0))
    bridge=bridge.union(panel(20.5,37.5,plane,.72,True)).union(box(.8,2.6,1.1,145.2,y+7.7,80))
for sign in [-1,1]:
    plane=cq.Plane(origin=(78.75,sign*68,92.75),xDir=(-sign,0,0),normal=(0,sign,0))
    bridge=bridge.union(panel(20.5,37.5,plane,.72,True))
add('09_stuurhut_met_deurkozijnen',bridge)

# Roof hood with three aft windows and a separate top to avoid the large bridge.
roof_pts=[(21,-50),(43,-72),(137,-72),(149,-60),(149,60),(137,72),(43,72),(21,50)]
hood_pts=[(25,-45),(40,-60),(122,-60),(122,60),(40,60),(25,45)]
roof=poly(roof_pts,2,113)
opening=cq.Workplane('XY').add(inset_wire(hood_pts,3,112)).toPending().extrude(4)
roof=roof.cut(opening)
ho=cq.Solid.makeLoft([wire(hood_pts,115),inset_wire(hood_pts,11,126)],ruled=True)
hi=cq.Solid.makeLoft([inset_wire(hood_pts,1.8,114),inset_wire(hood_pts,14.8,127)],ruled=True)
hood=cq.Workplane(obj=ho.cut(hi)).intersect(box(250,250,9,80,0,115))
for y in [-30,0,30]:hood=hood.cut(box(24,22,4.5,119,y,118))
roof=roof.union(hood)
socket=cq.Workplane('XY').center(138,0).circle(5).extrude(6).translate((0,0,115))
roof=roof.union(socket).cut(cq.Workplane('XY').center(138,0).circle(1.65).extrude(10).translate((0,0,112)))
add('10_dak_met_lichtkapwanden',roof,roof=True,note='Kleine lichtkapraambruggen controleren; kap is boven open tot deksel geplaatst wordt.')
cap=cq.Workplane(obj=ho).intersect(box(250,250,2,80,0,124))
add('11_lichtkap_deksel',cap,roof=True,rotate=True,note='Vlakke bovenzijde op bed; na beglazen op kap lijmen.')

def grille(wb,wt,h):
    pts=[(-wb/2,-h/2),(wb/2,-h/2),(wt/2,h/2),(-wt/2,h/2)]
    out=poly(pts,.28,-.14)
    fr=poly(pts,.65,.12).cut(cq.Workplane('XY').add(inset_wire(pts,.9,-1)).toPending().extrude(4))
    out=out.union(fr)
    count=min(12,max(3,int((h-4)/1.6)+1))
    for i in range(count):
        y=-h/2+2+(h-4)*i/(count-1);w=wb+(wt-wb)*(y+h/2)/h
        rib=box(w-1,1,.65,0,y,.12)
        out=out.union(rib.intersect(poly(pts,2,-.5)))
    return out

funnel_outers=[]
for sign,label,flange_i in [(1,'bakboord',15),(-1,'stuurboord',17)]:
    y=sign*77.5
    outer=cq.Solid.makeLoft([rwire(60,44,3,280,y,50),rwire(42,30,3,280,y,184)],ruled=True)
    hole=cq.Solid.makeLoft([rwire(56,40,1,280,y,49),rwire(38,26,1,280,y,185)],ruled=True)
    funnel=add_logo(cq.Workplane(obj=outer.cut(hole)),ROOT/'inputs/smitlogo.svg',sign)
    s=7/134;n=math.sqrt(1+s*s)
    plane=cq.Plane(origin=(296,sign*(55.5+22*s),72),xDir=(sign,0,0),normal=(0,-sign/n,s/n))
    funnel=funnel.union(on_plane(grille(14,11.5,32),plane))
    s=9/134;n=math.sqrt(1+s*s)
    plane=cq.Plane(origin=(310-22*s,sign*66.5,72),xDir=(0,1,0),normal=(1/n,0,s/n))
    funnel=funnel.union(on_plane(grille(12,10,32),plane))
    add('12_schoorsteen_logo_roosters_'+label,funnel,note='Logo en twee hoekroosters integraal meegeprint; brede voet op bed, brim mogelijk.')
    add('13_schoorsteenflens_'+label,OLD[flange_i])
    funnel_outers.append(outer)

# Connector with rounded central platform and small printed fitting.
beam=rounded(12,132,4,280,0,154,2)
pad=cq.Workplane('XY').center(283,0).ellipse(11,15).extrude(2.5).translate((0,0,157.5))
beam=beam.union(pad).union(cq.Workplane('XY').center(283,0).circle(1.6).extrude(5).translate((0,0,160)))
gusset=cq.Workplane('XZ').polyline([(278,160),(283,164.5),(288,160)]).close().extrude(.6,both=True)
beam=beam.union(gusset)
for o in funnel_outers:beam=beam.cut(cq.Workplane(obj=o))
add('14_dwarsverbinding_met_platform',beam,note='Brede vlakke balkonderzijde op bed.')

# Windbreak halves, divided by the front access opening.
wind=fore(70,205,16,71,-3).cut(fore(71,201,18,70,-1))
wind=wind.intersect(cq.Workplane('XZ').polyline([(0,71),(68,71),(46,87),(0,87)]).close().extrude(250,both=True))
wind=wind.cut(box(12,14,20,1,0,70))
for sign,label in [(1,'bakboord'),(-1,'stuurboord')]:
    half=wind.intersect(box(100,110,25,40,sign*55,70))
    add('15_windscherm_'+label,half)

floor_pts=[(183,-36.7),(205,-54.5),(320,-54.5),(320,54.5),(205,54.5),(183,36.7)]
floor=poly(floor_pts,3).cut(base)
add('16_achtervloer',floor,note='Dekt de aangenomen centrale rompopening af; vloerpassing nog op echte romp controleren.')

# Front boxes, open underneath; backs provide full glue faces against the house.
for y,label in [(15,'bakboord'),(-15,'stuurboord')]:
    case=rounded(14,28,28,-4,y,3,2).cut(rounded(10,24,26,-4,y,2,1))
    plane=cq.Plane(origin=(-11,y,17),xDir=(0,-1,0),normal=(-1,0,0))
    case=case.union(panel(21,22,plane,.72,True))
    add('17_voorkast_'+label,case,note='Hol, onderrand op bed; tegen voorwand lijmen. Steekt 11 mm voor bestaande X=0 uit.')

# Stepped cabinet/step feature at port of the aft recess; shape follows photos, function unverified.
step=box(28,18,20,211,-43.5,3).union(box(19,18,11,206.5,-43.5,23)).union(box(10,18,14,202,-43.5,34))
step=step.cut(main_outer).cut(upper)
for y in [-47.8,-39.2]:
    plane=cq.Plane(origin=(225,y,13),xDir=(0,1,0),normal=(1,0,0))
    step=step.union(panel(7,15,plane,.65,True))
add('18_achterkast_getrapt',step)

case=rounded(14,44,13,192,12,3,1.5)
case=case.cut(rounded(10,40,11,192,12,2,.8))
for y in [1,23]:
    plane=cq.Plane(origin=(199,y,9.5),xDir=(0,1,0),normal=(1,0,0))
    case=case.union(panel(15,8,plane,.65,True))
add('19_achterkast_laag',case)
right=cq.Workplane('XZ').polyline([(199,3),(218,3),(218,20),(199,25)]).close().extrude(8.5,both=True).translate((0,43.5,0))
right=right.cut(main_outer)
plane=cq.Plane(origin=(218,43.5,11),xDir=(0,1,0),normal=(1,0,0))
right=right.union(panel(12,14,plane,.65,True))
add('20_achterkast_schuin',right)

# Five separate grille panels shown near the aft upper-house wall in the references.
# These installation positions remain an explicit prototype assumption.
for i,(y,w) in enumerate([(-70,10),(-35,14),(0,9),(35,14),(70,14)],1):
    g=grille(w,w,14).translate((0,0,.14))
    n=math.sqrt(1+slope*slope)
    plane=cq.Plane(origin=(185-(55.5-45)*slope,y,55.5),xDir=(0,1,0),normal=(1/n,0,slope/n))
    add(f'21_bovendekrooster_{i}',on_plane(g,plane),note='Los rooster; plaatsing op schuine achterwand is een aanname. Vlakke achterzijde op bed.',print_shape=g)

add('22_lijmstrip_4x',box(30,12,2),qty=4,include=False,note='Vrij te plaatsen binnenversterking; zo nodig inkorten.')
add('23_aanslagblok_4x',box(10,4,4),qty=4,include=False)

def mesh(s,roof=False):
    v,f=s.tessellate(.22,.22)
    return dict(v=[c for p in v for c in [round(p.x-160,3),round(p.y,3),round(p.z-80,3)]],f=[i for t in f for i in t],roof=roof)
(ROOT/'viewer_mesh.json').write_text(json.dumps({'v1':[mesh(s,i==13) for i,s in enumerate(OLD)],'study':[mesh(s,r) for n,s,r in parts]},separators=(',',':')))
compound=cq.Compound.makeCompound([s for n,s,r in parts])
cq.exporters.export(compound,str(ROOT/'STEP/SL109_v4_assemblage.step'))

# Volume interference test on all assembled primary and detail parts.
collisions=[]
for i,(an,a,_) in enumerate(parts):
    ba=a.BoundingBox()
    for bn,b,_ in parts[i+1:]:
        bb=b.BoundingBox()
        if min(ba.xmax,bb.xmax)-max(ba.xmin,bb.xmin)<=.001:continue
        if min(ba.ymax,bb.ymax)-max(ba.ymin,bb.ymin)<=.001:continue
        if min(ba.zmax,bb.zmax)-max(ba.zmin,bb.zmin)<=.001:continue
        volume=a.intersect(b).Volume()
        if volume>.05:collisions.append(dict(a=an,b=bn,volume_mm3=round(volume,4)))
(ROOT/'interferenties.json').write_text(json.dumps(collisions,indent=2))
(ROOT/'controle.json').write_text(json.dumps({'parts':records,'collisions':collisions,'status':'geometry checked; no physical print or slicer test'},indent=2))
with (ROOT/'onderdelen.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['onderdeel','aantal','X_mm','Y_mm','Z_mm','volume_cm3','printstand','opmerking'])
    for p in records:w.writerow([p['part'],p['qty'],*p['print_mm'],p['volume_cm3'],p['orientation'],p['note']])
assert not collisions,collisions
print('VALIDATED',len(records),'unique STL files; no volume collisions',flush=True)
