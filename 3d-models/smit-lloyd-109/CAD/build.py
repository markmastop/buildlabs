"""Smit-Lloyd 109 v18. Millimetres. Measured lower house plus photographic upperwork.
Run with CadQuery 2.8: python CAD/build.py. All editable dimensions: parameters.json.
See metingen.json for measurement definitions. No claim of historical drawing accuracy.
"""
from pathlib import Path
import json,csv,math
import cadquery as cq
import trimesh
from smit_logo import relief
from bridge import make_bridge
import voetafdruk
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'CAD/parameters.json').read_text());M=P['measured'];C=P['construction'];U=P['upper'];A=P['aft'];B=P['connector'];SIDE=P['sides'];N=P['anchor_niche']
W=C['wall'];T=C['deck'];L=M['length'];Z=M['aft_deck_height'];FZ=M['fore_roof_height'];SPLIT=C['lower_split_x']
for d in ['STL','STEP']:(ROOT/d).mkdir(exist_ok=True)
parts=[];records=[];objects={};validation={}
OLD=cq.importers.importStep(str(ROOT/U['reference_file'])).solids().vals()
assert len(OLD)==32
assert abs(OLD[11].BoundingBox().zmin-71)<.001

def box(dx,dy,dz,x=0,y=0,z=0):return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,False)).translate((x,y,z))
def poly(pts,h,z=0):return cq.Workplane('XY').polyline(pts).close().extrude(h).translate((0,0,z))
def rounded(dx,dy,h,x=0,y=0,z=0,r=1):return box(dx,dy,h,x,y,z).edges('|Z').fillet(r)
def clip(shape,x0,x1,z0=-20,z1=250):return shape.intersect(box(x1-x0,500,z1-z0,(x0+x1)/2,0,z0))
def aswp(s):return s if isinstance(s,cq.Workplane) else cq.Workplane(obj=s)
def shifted(s,dx=0,dy=0,dz=0,sx=1,sy=1,sz=1):
    return cq.Workplane(obj=s.transformGeometry(cq.Matrix([[sx,0,0,dx],[0,sy,0,dy],[0,0,sz,dz],[0,0,0,1]])))
def add(name,shape,*,roof=False,base=False,flip=False,qty=1,include=True,note='',print_shape=None):
    # Export axes: X aft, Y toward photo-left, Z up. Internal sketch uses the opposite Y.
    shape=cq.Workplane(obj=aswp(shape).val().mirror('XZ')).clean();ss=shape.solids().vals()
    if len(ss)!=1:
        print('DISCONNECTED',name,[(q.Volume(),[getattr(q.BoundingBox(),k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']]) for q in ss],flush=True)
    assert len(ss)==1 and ss[0].isValid(),(name,'invalid or disconnected BRep',len(ss))
    objects[name]=shape
    out=aswp(print_shape) if print_shape is not None else shape
    if flip:out=out.rotate((0,0,0),(1,0,0),180)
    b=out.val().BoundingBox();out=out.translate((-b.xmin,-b.ymin,-b.zmin))
    if name == '00_pasproef':
        folder = ROOT / 'pasmal'
        folder.mkdir(exist_ok=True)
        stl = folder / (name + '.stl')
        step = folder / (name + '.step')
    else:
        stl = ROOT / 'STL' / (name + '.stl')
        step = ROOT / 'STEP' / (name + '.step')
    cq.exporters.export(out,str(stl),tolerance=.035,angularTolerance=.12);cq.exporters.export(out,str(step))
    mesh=trimesh.load_mesh(stl,process=True)
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0 and len(mesh.split())==1,(name,'STL topology')
    assert max(mesh.extents[:2])<=P['print']['max_footprint'],(name,'bed',mesh.extents)
    record=dict(part=name,qty=qty,print_mm=mesh.extents.round(3).tolist(),volume_cm3=round(mesh.volume/1000,4),orientation='bovenzijde op bed' if flip else ('voorgeorienteerd; zie opmerking' if print_shape is not None else 'onderzijde op bed'),assembled=include,roof=roof,measured_base=base,note=note)
    records.append(record)
    if include:parts.append((name,ss[0],roof,base))
    print(name,'OK',mesh.extents.round(2).tolist(),flush=True)
    return shape

def nose_points(width):
    # Fine polygon approximation avoids the OCCT STEP loss of long elliptic extrusion faces.
    # 96 segments: maximum chord error below 0.05 mm for this assumed 35 x 90 nose.
    return voetafdruk.nose_points(P,width)
def fore_wire(length,width,z=0):
    s=(cq.Workplane('XY').polyline(nose_points(width)).lineTo(length,width/2).lineTo(length,-width/2).close())
    wire=s.wire().val();b=wire.BoundingBox();assert abs(b.xmin)<.001 and abs(b.xmax-length)<.001,(b.xmin,b.xmax)
    return wire.translate(cq.Vector(0,0,z))
def wire_solid(w,h):return cq.Workplane('XY').add(w).toPending().extrude(h)
def offset_wire(w,inset):return cq.Workplane('XY').add(w).toPending().offset2D(-inset,kind='intersection').val()
def on_plane(shape,plane):return cq.Workplane(obj=shape.val().transformShape(plane.rG))
def panel(w,h,plane,depth=.6,outline=False):
    s=rounded(w,h,depth,0,0,-.12,min(1,w/8))
    if outline:s=s.cut(rounded(w-1.6,h-1.6,depth+2,0,0,-1,min(.5,w/12)))
    return on_plane(s,plane)

# Analytic nose ellipse and measured aft widths/stations. All small radii/offsets listed as assumptions.
# V18: the shared footprint module follows the real moulded part (flat block, straight U,
# notch, inward-tapering arm ends, rounder corners). See voetafdruk.py.
S=voetafdruk.stations(P)
H=S['H'];yiL=S['yiL'];yiR=S['yiR'];UX=S['UX'];l3=S['l3'];l4=S['l4'];r3=S['r3'];r4=S['r4']
lout=S['lout'];rheadinner=S['rheadinner'];rheadouter=S['rheadouter'];nt=S['nt'];nr=C['fore_nose_depth']
wp=cq.Workplane('XY').polyline(voetafdruk.outline_points(P)).close()
outline=wp.wire().val();bb=outline.BoundingBox();assert abs(bb.xmin)<.001 and abs(bb.xmax-L)<.001
assert abs(bb.ymin-lout)<.001 and abs(bb.ymax-rheadouter)<.001
outer=wire_solid(outline,Z)
inner=wire_solid(offset_wire(outline,W),Z+2).translate((0,0,-1))
shell=outer.cut(inner).intersect(box(500,500,Z-T,190,0,0))

# Photo-derived lower window stations: four ahead of the module joint and two aft.
# A/B have separate parameter lists even though the user confirms the same layout.
for side in ['A','B']:
    sign=SIDE[side]['internal_sign']
    for win in SIDE[side]['lower_windows']:
        cutter=box(win['width'],28,win['height'],win['x'],sign*88,win['bottom']).edges('|Y').fillet(win['corner_radius'])
        shell=shell.cut(cutter)
# Rear-photo convention: r increases from photo-left to photo-right.
# Internal Y therefore decreases with r. Only aft details change sides; measured hull footprint stays.
for r in A['window_r']:shell=shell.cut(box(10,A['window_width'],A['window_height'],UX,yiR-r,A['window_bottom']))
# V18: the inner block of the broad arm stays a flat part of the moulded shell, as on the real part.
# Four ceiling tabs keep the frame flange inside the shell: deck datum stays at zero.
for x in C['frame_tab_x']:
    for sign in [-1,1]:shell=shell.union(box(30,C['frame_tab_width'],C['frame_tab_thickness'],x,sign*C['frame_tab_y'],C['frame_flange'][2]).intersect(outer))
shell_baseline=shell
# One-sided anchor pocket: an integral return/back/sill replaces a strip of thin skin.
# Z=3 sill underside clears the unchanged frame flange at Z=2.
ns=SIDE[N['side']]['internal_sign'];nx0=N['x_front'];nx1=N['x_rear'];nb=N['back_y'];nw=N['backing']
ni=(nb-nw+120)/2
blank=box(nx1-nx0+2*nw,120-(nb-nw),Z-T-(N['sill_top']-N['sill_thickness']),(nx0+nx1)/2,ns*ni,N['sill_top']-N['sill_thickness']).intersect(outer)
void=box(nx1-nx0,120-nb,Z-T-N['sill_top']+1,(nx0+nx1)/2,ns*(nb+120)/2,N['sill_top'])
shell=shell.union(blank).cut(void)
add('02_onderdekhuis_voor',clip(shell,-1,SPLIT),base=True,note='V17: zijde A vier voorste ramen; zijde B twee voorste ramen en gesloten ankernis. Rechtop printen; nisplafond is deel 04. Pasframevlakken blijven vrij.')
add('03_onderdekhuis_achter',clip(shell_baseline,SPLIT,L+1),base=True,note='V18: vlak blok aan de brede arm met inkeping, rechte U-bodem met R2, armuiteinden R8 die binnen schuin naar buiten lopen. Twee kleine ramen per zijde achter de naad. Rechtop printen.')

# Fitting ring, independent of the house. Its flange is inside the lower house (Z 0..2), insertion Z -6..0.
def frame(wall):
    fx,fy=C['frame_center_x'],C['frame_center_y'];a,b=C['frame_outer'];flx,fly,flz=C['frame_flange']
    tongue=box(a,b,C['frame_insert_depth'],fx,fy,-C['frame_insert_depth']).cut(box(a-2*wall,b-2*wall,C['frame_insert_depth']+2,fx,fy,-C['frame_insert_depth']-1))
    flange=box(flx,fly,flz,fx,fy,0).cut(box(a-2*wall,b-2*wall,flz+2,fx,fy,-1))
    return tongue.union(flange)
add('00_pasproef',frame(1.6),base=True,flip=True,include=False,note='Eerst volledig passen in 205 x 153 mm opening. Niet forceren; controleer ook hoekradius en dekdikte.')
add('01_pasframe',frame(C['frame_wall']),base=True,flip=True,note='Los droogpassen; definitieve lengtepositie op echte romp bepalen vóór verlijmen. Flens intern op Z 0..2.')

# Lower roof around the upper tier, split at the same station as the walls.
low_roof=wire_solid(outline,T).translate((0,0,Z-T))
plen=M['fore_roof_length']+C['upper_rear_slope_run']
forebottom=fore_wire(plen,M['front_width'],Z)
foretop=fore_wire(M['fore_roof_length'],M['front_width'],FZ)
upper_outer=cq.Solid.makeLoft([forebottom,foretop],ruled=True)
low_roof=low_roof.cut(wire_solid(offset_wire(fore_wire(plen,M['front_width']),W),8).translate((0,0,Z-4)))
low_roof_baseline=low_roof
# Close the new pocket above; this ceiling belongs to the horizontal deck module.
niche_ceiling=box(nx1-nx0+2*nw,120-(nb-nw),T,(nx0+nx1)/2,ns*ni,Z-T).intersect(outer)
low_roof=low_roof.union(niche_ceiling)
add('04_achterdek_voor',clip(low_roof,-1,SPLIT),base=True,note='V17: vlak printen. Ring rond hoger voordek plus plafond ankernis aan zijde B. Eerst zijraambeglazing plaatsen; nieuwe nis droogpassen.')
add('05_achterdek_achter',clip(low_roof_baseline,SPLIT,L+1),base=True,note='Vlak printen. Meetbasis op Z=60 mm; U blijft open zoals origineel.')
# An offset in horizontal sections is a controlled prototype wall choice on the sloping rear face.
ib=offset_wire(fore_wire(plen,M['front_width'],Z-1),W)
it=offset_wire(fore_wire(M['fore_roof_length'],M['front_width'],FZ+1),W)
upper_inner=cq.Solid.makeLoft([ib,it],ruled=True)
upper=aswp(upper_outer.cut(upper_inner)).intersect(box(500,500,FZ-Z-T,190,0,Z))
# Closed photographic recesses: preserve an integral backing, then cut a drafted
# pocket that follows the polygonal nose. Every face below is planar; this avoids
# the STEP ellipse-face loss previously observed in this project.
def side_surface_y(xx):
    pts=nose_points(M['front_width'])
    pos=sorted((x,y) for x,y in pts if y>=-1e-8)
    if xx>=pos[-1][0]:return M['front_width']/2
    for (xa,ya),(xb,yb) in zip(pos,pos[1:]):
        if xa-1e-8<=xx<=xb+1e-8:
            return ya+(yb-ya)*(xx-xa)/(xb-xa)
    raise ValueError(xx)

def recessed_cutter(cfg,sign):
    xx=cfg['x'];w=cfg['width'];z0=cfg['bottom'];z1=z0+cfg['height']
    dep=cfg['depth_y'];bevel=cfg['return_run'];x0=xx-w/2;x1=xx+w/2
    stations={x0,x0+bevel,x1-bevel,x1}
    stations.update(x for x,y in nose_points(M['front_width']) if y>=0 and x0<x<x1)
    stations=sorted(stations);rings=[]
    for x in stations:
        fraction=max(0,min(1,(x-x0)/bevel,(x1-x)/bevel))
        y=side_surface_y(x);depth=dep*fraction;rise=bevel*fraction
        rings.append([(x,sign*120,z0),(x,sign*120,z1),
                      (x,sign*y,z1),(x,sign*(y-depth),z1-rise),
                      (x,sign*(y-depth),z0+rise),(x,sign*y,z0)])
    faces=[]
    def triangle(a,b,c):
        va,vb,vc=map(cq.Vector,[a,b,c])
        if (vb-va).cross(vc-va).Length<1e-9:return
        faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon([va,vb,vc,va])))
    for ra,rb in zip(rings,rings[1:]):
        for j in range(6):
            k=(j+1)%6
            triangle(ra[j],rb[j],rb[k]);triangle(ra[j],rb[k],ra[k])
    for ring,reverse in [(rings[0],True),(rings[-1],False)]:
        clean=[]
        for pt in ring:
            if not clean or (cq.Vector(pt)-cq.Vector(clean[-1])).Length>1e-7:clean.append(pt)
        if (cq.Vector(clean[0])-cq.Vector(clean[-1])).Length<1e-7:clean.pop()
        face=cq.Face.makeFromWires(cq.Wire.makePolygon([cq.Vector(q) for q in clean+[clean[0]]]))
        if reverse:face.wrapped.Reverse()
        faces.append(face)
    result=cq.Solid.makeSolid(cq.Shell.makeShell(faces))
    if result.Volume()<0:result.wrapped.Reverse()
    assert result.isValid() and result.Volume()>0,'invalid pocket cutter'
    return aswp(result)

for side in ['A','B']:
    sign=SIDE[side]['internal_sign']
    for cfg in SIDE[side]['upper_recesses']:
        deep=cfg['depth_y']+cfg['backing_y']
        band=aswp(upper_outer).cut(upper_outer.translate(cq.Vector(0,-sign*deep,0)))
        region=box(cfg['width']+2*W,70,cfg['height']+2*W,cfg['x'],sign*90,cfg['bottom']-W)
        upper=upper.union(band.intersect(region)).cut(recessed_cutter(cfg,sign))
add('06_verhoogd_voordekhuis',upper,base=True,note='V17: twee gesloten nissen per kant; diepte 8 mm in Y, schuine aansluitingen 2,5 mm. Achterwand integraal, voorste nis volgt ronding. Foto-inschattingen. Open schaal rechtop printen.')
forelid=aswp(upper_outer).intersect(box(500,500,T,190,0,FZ-T))
add('07_voordak_163mm',forelid,base=True,flip=True,note='Vlakke bovenzijde op bed. Lengte bovenzijde 163 mm, breedte 180 mm; gemeten dakhoogte 86 mm.')

# Measured front boxes. Back faces are trimmed to the analytic curved house wall; projections remain parametric.
def case_on_fore(width,projection,height,y=0,notch=0):
    # Wall X at the case centre on the elliptical forward face. Dims are protrusion at centre, not a rectangular rear depth.
    back=nr-nr*math.sqrt(max(0,1-(y/(M['front_width']/2))**2))
    front=back-projection
    raw=rounded(projection+nr+5,width,height,front+(projection+nr+5)/2,y,C['front_box_z'],C['front_box_corner_radius'])
    raw=raw.cut(outer)
    raw=raw.intersect(box(projection+nr+10,width+4,height+2,front+(projection+nr+10)/2,y,C['front_box_z']-1))
    # Open underside, with a constant 2 mm front wall and side walls.
    cavity=box(projection+nr+5-W,width-2*W,height-W,front+W+(projection+nr+5-W)/2,y,C['front_box_z']-1)
    raw=raw.cut(cavity)
    if notch:
        # Full-height vertical channel, closed behind the groove. Reinforcement
        # joins both sides of the hollow shell without changing its outer bounds.
        backwall=C['front_groove_backing']
        reinforcement=box(notch+backwall,2*(notch+backwall),height,front+(notch+backwall)/2,y,C['front_box_z'])
        raw=raw.union(reinforcement)
        groove=cq.Workplane('XY').center(front,y).circle(notch).extrude(height+2).translate((0,0,C['front_box_z']-1))
        raw=raw.cut(groove)
    return raw,front
cb=M['front_center_box'];sb=M['front_small_box']
center,center_front=case_on_fore(*cb,y=0,notch=C['front_center_notch_radius'])
small_y=-(cb[0]/2+sb[0]/2+C['front_small_box_gap'])
small,small_front=case_on_fore(*sb,y=small_y)
add('08_middenblok_65x25x55',center,base=True,note='V18: gemeten 65 breed x 25 uitsteek x 55 hoog, staande hoeken R6. Verticale groef over volle hoogte, voorlopig R4 met 2 mm gesloten rug. Holle onderzijde op bed; groef niet vullen.')
add('09_klein_blok_links_25x15x30',small,base=True,note='V18: gemeten breedte 25, uitsteek 15 en hoogte 30 mm, staande hoeken R6. Links van middenblok zoals foto; onderkant Z=0 aangenomen.')

# Independent editable wheelhouse replaces the inherited v4 solids.
bs=U['bridge_z_shift']
bridge_body,bridge_roof,bridge_cap,bridge_report,cap_edge=make_bridge(P['bridge'])
add('10_stuurhut_met_raamopeningen',bridge_body,note='V17: wand 55 hoog, voet 90 lang, breedte 136. Extra hoogte onder ramen; glasvormen behouden. Rechte deur, apart schuin raam en compactere zijramen. Dunne kozijnen; geen donkere ondervlakjes. Voet op bed. Alle detailmaten foto-inschattingen.')
add('11_stuurhutdak_lichtkap',bridge_roof,roof=True,note='V17: dak voor kortere stuurhut, contact Z141. Overstek 3; kap eindigt X97 en is 14 mm hoog; vlak achterdak en 3 kleine kapramen. Vlakke onderzijde op bed. Overstekken en raambruggen in slicer beoordelen.')
add('12_lichtkap_deksel',bridge_cap,roof=True,note='V17: kaal 2 mm kapdeksel zonder rand of uitrusting. VLAKKE ONDERZIJDE op bed. Na beglazing op 11 lijmen.')

# New windbreak follows the measured-width roof, with central access gap, split L/R.
wind=wire_solid(fore_wire(68,M['front_width']),16).translate((0,0,FZ))
wind=wind.cut(wire_solid(offset_wire(fore_wire(69,M['front_width']),2),18).translate((0,0,FZ-1)))
wind=wind.intersect(cq.Workplane('XZ').polyline([(0,FZ),(68,FZ),(46,FZ+16),(0,FZ+16)]).close().extrude(220,both=True))
wind=wind.cut(box(20,C['front_railing_gap_width'],20,0,0,FZ-1)).cut(aswp(OLD[11]).translate((0,0,bs)))
for sign,label in [(-1,'L'),(1,'R')]:
    half=wind.intersect(box(150,100,20,40,sign*50,FZ))
    # Clearance around the existing bridge corner can leave a tiny detached end sliver.
    half=cq.Workplane(obj=max(half.solids().vals(),key=lambda a:a.Volume()))
    add('13_windscherm_'+label,half,note='Vlakke onderrand op bed, tegen stuurhutdakplint lijmen. Breedte aangepast aan 180 mm dak.')

def grille(wb,wt,h):
    pts=[(-wb/2,-h/2),(wb/2,-h/2),(wt/2,h/2),(-wt/2,h/2)]
    out=poly(pts,.28,-.14);fr=poly(pts,.65,.12).cut(cq.Workplane('XY').polyline(pts).close().offset2D(-.9).extrude(4).translate((0,0,-1)))
    out=out.union(fr);n=min(12,max(3,int((h-4)/1.6)+1))
    for i in range(n):
        y=-h/2+2+(h-4)*i/(n-1);w=wb+(wt-wb)*(y+h/2)/h
        out=out.union(box(w-1,1,.65,0,y,.12).intersect(poly(pts,2,-.5)))
    return out

def rwire(dx,dy,r,x,y,z):return rounded(dx,dy,1,x,y,z,r).faces('<Z').wires().val()
def grille_masks(wb,wt,h):
    pts=[(-wb/2,-h/2),(wb/2,-h/2),(wt/2,h/2),(-wt/2,h/2)]
    footprint=poly(pts,10,-5)
    rails=footprint.cut(cq.Workplane('XY').polyline(pts).close().offset2D(-.9).extrude(12).translate((0,0,-6)))
    count=12
    for j in range(count):
        yy=-h/2+2+(h-4)*j/(count-1);ww=wb+(wt-wb)*(yy+h/2)/h
        rails=rails.union(box(ww-1,1,10,0,yy,-5).intersect(footprint))
    return footprint,rails

funnel_outers=[];funnel_records=[]
# V18: the arm ends taper inward, so funnel and foot stay inside the deck outline
# (inset by a small margin). The cut becomes a flat inner facet with the same wall.
fm=U['funnel_facet_margin']
def inside_deck(inset):return wire_solid(offset_wire(outline,inset),400).translate((0,0,-50))
def facet_frame(sign):
    a=(S['taper_x'],S['yiL'] if sign<0 else S['rheadinner']);b=(L,S['left_end_inner'] if sign<0 else S['right_end_inner'])
    dl=math.hypot(b[0]-a[0],b[1]-a[1]);d=((b[0]-a[0])/dl,(b[1]-a[1])/dl)
    n=(-d[1],d[0]) if sign<0 else (d[1],-d[0])  # horizontal, toward the centre line
    return a,d,n
for sign,label,y,bw in [(-1,'L',U['left_funnel_y'],U['left_funnel_width']),(1,'R',U['right_funnel_y'],U['right_funnel_width'])]:
    x=U['funnel_center_x'];z=Z+U['funnel_flange_height'];h=U['funnel_height'];bl=U['funnel_length'];tl=U['funnel_top_length'];tw=bw-U['funnel_width_taper'];fw=U['funnel_wall'];rb=U['funnel_base_radius'];rt=U['funnel_top_radius']
    assert rb<bw/2 and rt<tw/2
    def loft_offset(delta):
        return aswp(cq.Solid.makeLoft([rwire(bl+2*delta,bw+2*delta,rb+delta,x,y,z),rwire(tl+2*delta,tw+2*delta,rt+delta,x,y,z+h)],ruled=True))
    def top_height(xx):return z+h-U['funnel_top_drop']*(xx-(x-tl/2))/tl
    cut_top=cq.Workplane('XZ').polyline([(x-150,z-2),(x+150,z-2),(x+150,top_height(x+150)),(x-150,top_height(x-150))]).close().extrude(250,both=True)
    out=loft_offset(0).intersect(cut_top).intersect(inside_deck(fm))
    hole=aswp(cq.Solid.makeLoft([rwire(bl-2*fw,bw-2*fw,rb-fw,x,y,z-1),rwire(tl-2*fw,tw-2*fw,rt-fw,x,y,z+h+1)],ruled=True)).intersect(inside_deck(fm+fw))
    funnel=out.cut(hole)
    rim_band=cut_top.cut(cut_top.translate((0,0,-U['funnel_top_rim_height'])))
    rim=loft_offset(U['funnel_top_rim_relief']).intersect(rim_band).intersect(inside_deck(fm-U['funnel_top_rim_relief'])).cut(hole)
    funnel=funnel.union(rim)
    logo=relief(ROOT/'inputs/smitlogo.svg',sign,width=U['logo_width'],height_center=U['logo_center_z'],depth=U['logo_relief'],x_center=x,y_center=y,z_bottom=z,base_width=bw,top_width=tw,total_height=h)
    funnel=funnel.union(logo)
    expanded_base=loft_offset(U['funnel_grille_base_relief']).intersect(inside_deck(fm-U['funnel_grille_base_relief']))
    expanded_ribs=loft_offset(U['funnel_grille_rib_relief']).intersect(inside_deck(fm-U['funnel_grille_rib_relief']))
    gh=U['funnel_grille_height'];za=U['funnel_grille_bottom']+gh/2
    sy=(bw-tw)/2/h;ny=math.sqrt(1+sy*sy)
    # The inner corner grille sits on the new flat facet, fully within its height.
    fa,fd,fn=facet_frame(sign);gx=U['funnel_inner_grille_x']
    # Point on the arm's taper line at X=gx, moved inward by the same margin as the facet.
    gp=(gx-fm*fn[0],fa[1]+fd[1]/fd[0]*(gx-fa[0])-fm*fn[1])
    inner_plane=cq.Plane(origin=(gp[0],gp[1],z+za),xDir=(sign*fd[0],sign*fd[1],0),normal=(fn[0],fn[1],0))
    sx=(bl-tl)/2/h;nx=math.sqrt(1+sx*sx)
    end_plane=cq.Plane(origin=(x+bl/2-za*sx,y,z+za),xDir=(0,1,0),normal=(1/nx,0,sx/nx))
    for plane,wb,wt in [(inner_plane,U['funnel_inner_grille_bottom_width'],U['funnel_inner_grille_top_width']),(end_plane,U['funnel_end_grille_bottom_width'],U['funnel_end_grille_top_width'])]:
        fp,rails=grille_masks(wb,wt,gh)
        # The masks are intersected with expanded round lofts: the relief follows
        # the real curved wall, instead of leaving a flat grille floating at a corner.
        backing=on_plane(fp,plane).intersect(expanded_base)
        ribs=on_plane(rails,plane).intersect(expanded_ribs)
        funnel=funnel.union(backing).union(ribs)
    funnel=funnel.cut(hole)
    add('15_schoorsteen_logo_roosters_'+label,funnel,note='V18: achteraan binnen versmald met een vlak facet langs de schuine armrand; binnenrooster op het facet. Rondingen R12/R10; lengte 80/62. SMIT en twee hoekroosters integraal. Bovenzijde open. Foto-aannames. Brede onderrand op bed.')
    flange_radius=(bw+2)/2-U['funnel_flange_radius_margin']
    flange=rounded(bl+4,bw+2,U['funnel_flange_height'],x,y,Z,flange_radius).intersect(inside_deck(fm))
    flange=flange.cut(rounded(bl-2*fw,bw-2*fw,U['funnel_flange_height']+2,x,y,Z-1,rb-fw).intersect(inside_deck(fm+fw)))
    add('14_schoorsteenvoet_'+label,flange,note='V18: afgeronde voetplaat, 84 lang, achteraan binnen ingekort tot binnen de schuine armrand. Zelfde montagecentrum als v7. Vlak op bed; bovenkant voet op Z=62.')
    funnel_outers.append(out.val())
    funnel_records.append(dict(label=label,inner_facet=dict(margin=fm,grille_center_x=gx,grille_origin=list(gp),direction=list(fd)),center_x=x,internal_center_y=y,base_z=z,height=h,base_length=bl,top_length=tl,base_width=bw,top_width=tw,base_radius=rb,top_radius=rt,top_drop=U['funnel_top_drop'],grille_height=gh,grille_bottom=U['funnel_grille_bottom']))

# Top-view photo: a flat plate with a widened, aft-projecting middle platform.
cy=(U['left_funnel_y']+U['right_funnel_y'])/2;span=U['right_funnel_y']-U['left_funnel_y'];x=U['funnel_center_x'];bz=U['connector_z'];bt=B['plate_thickness']
beam=box(B['arm_width'],span,bt,x,cy,bz)
pp=[(x+B['platform_front_offset'],cy-B['platform_half_span']),(x+B['arm_width']/2,cy-B['platform_half_span']),(x+B['platform_rear_offset'],cy-B['platform_rear_half_width']),(x+B['platform_rear_offset'],cy+B['platform_rear_half_width']),(x+B['arm_width']/2,cy+B['platform_half_span']),(x+B['platform_front_offset'],cy+B['platform_half_span'])]
platform=poly(pp,bt,bz).edges('|Z').fillet(B['platform_corner_radius'])
beam=beam.union(platform)
px=x+B['boss_x_offset'];boss=cq.Workplane('XY').center(px,cy).circle(B['boss_outer_diameter']/2).extrude(B['boss_height']).translate((0,0,bz+bt))
beam=beam.union(boss)
for side in [-1,1]:
    fin=cq.Workplane('XZ').polyline([(px+side*2,bz+bt-.1),(px+side*5,bz+bt-.1),(px+side*2,bz+bt+B['boss_height'])]).close().extrude(B['gusset_thickness']/2,both=True).translate((0,cy,0))
    beam=beam.union(fin)
beam=beam.cut(cq.Workplane('XY').center(px,cy).circle(B['boss_inner_diameter']/2).extrude(B['boss_height']+.1).translate((0,0,bz+bt)))
for ss in funnel_outers:beam=beam.cut(aswp(ss))
add('16_dwarsverbinding_met_platform',beam,note='V8: vlakke plaat met in bovenaanzicht verbreed, naar achter uitstekend middenplatform. Kleine ring met twee schoren. Brede vlakke onderzijde op bed; foto-aannames.')

# Five loose upper grilles on the sloping rear face, just above the measured lower deck.
slope=C['upper_rear_slope_run']/(FZ-Z);norm=math.sqrt(1+slope*slope)
for i,y in enumerate([-65,-32.5,0,32.5,65],1):
    g=grille(12,12,13).translate((0,0,.14));gz=72
    plane=cq.Plane(origin=(plen-(gz-Z)*slope,y,gz),xDir=(0,1,0),normal=(1/norm,0,slope/norm))
    add(f'20_rooster_bovenhuis_{i}',on_plane(g,plane),print_shape=g,note='Los rooster; locatie en maat uit fotoprototype aangenomen. Vlakke rug op bed.')

# Optional lower U floor is deliberately separate: original mould is open and frame position is not verified.
floor=box(M['U_depth_left'],M['U_width'],T,UX+M['U_depth_left']/2,(yiL+yiR)/2,0).cut(outer)
# Preserve a 0.15 mm fitting gap to the house sides.
floor=clip(floor,UX+.15,L-.15).intersect(box(150,M['U_width']-.3,T,UX+57.5,(yiL+yiR)/2,0))
add('21_achtervloer_optioneel',floor,include=False,note='Optioneel: centrale U-vloer tussen de armen. Niet in assemblage opgenomen; de echte opbouw is open. Werkelijk pasframe eerst passen.')
add('22_lijmstrip_4x',box(30,12,2),qty=4,include=False,note='Binnen langs lengtenaad onderdekhuis lijmen, vrij plaatsen/inkorten.')
add('23_dek_lijmstrip_4x',box(24,8,2),qty=4,include=False,note='Onder de deknaden, vrij plaatsen vóór montage.')

# Readback and dimensional checks.
assembly=cq.Compound.makeCompound([s for n,s,r,b in parts]);ab=assembly.BoundingBox()
validation['measured_dimensions']=dict(length=L,front_width=M['front_width'],fore_roof_top_length=M['fore_roof_length'],aft_roof_z=Z,fore_roof_z=FZ,U_width=yiR-yiL,U_depth_left=L-UX,U_depth_right=L-UX,left_narrow=M['left_narrow'],right_with_block=H-yiR,right_bare=M['right_bare'],left_shoulder_run=l3-l4,right_shoulder_run=r3-r4)
validation['datum']='Z=0 is rompdek/onderrand huis; pasframe-insteek tot Z=-6. Exportassen: X naar achteren, Y naar foto-links, Z omhoog. Cross_sections gebruiken interne Y-as met tegengesteld teken.'
validation['assembly_bounds']=[ab.xmin,ab.xmax,ab.ymin,ab.ymax,ab.zmin,ab.zmax]
validation['assembly_size']=[ab.xlen,ab.ylen,ab.zlen]
validation['frame_position_status']='PROVISIONAL X=160; slide fit to actual hull before gluing'
validation['status']='Geometry checked; no physical fit or print/slicer layer validation yet'
# Actual geometric probes verify the station widths, including the right notch measurement.
def intervals_at(x):
    probe=outer.intersect(box(.002,500,1,x,0,10)).solids().vals()
    return sorted([(s.BoundingBox().ymin,s.BoundingBox().ymax) for s in probe])
validation['cross_sections']={str(x):intervals_at(x) for x in [100,280,302.5,307.5,320,325,335,350,370,380]}
validation['bridge_revision']=bridge_report
validation['simplification']=dict(solid_front_windbreak_restored_from='v12',other_railings=False,roof_equipment=False,lifebuoys=False,roof_rim=False,mast_bore=False)
validation['front_revision']=dict(full_height_groove=True,groove_radius=C['front_center_notch_radius'],groove_backing=C['front_groove_backing'],groove_height=M['front_center_box'][2],railing_gap_width=C['front_railing_gap_width'],railing_gap_bottom=FZ,railing_gap_top=FZ+16,dimensions_status='groove and gap detail sizes are photographic assumptions')
validation['side_windows']=dict(A=SIDE['A'],B=SIDE['B'],same_layout_confirmed_by_user=False,anchor_one_side_confirmed_by_user=True,lower_count=dict(A=6,B=4),upper_recess_count_per_side=2,lower_joint_distribution=dict(A=[4,2],B=[2,2]),dimension_status='photo estimates, not measured')
validation['anchor_niche']=dict(**N,cavity_top=Z-T,backing_bottom=N['sill_top']-N['sill_thickness'],frame_flange_clearance=N['sill_top']-N['sill_thickness']-C['frame_flange'][2])
validation['funnel_revision']=dict(parts=funnel_records,connector=dict(flat_plate=True,plate_thickness=B['plate_thickness'],planform_platform=pp),status='Photographic prototype; radii and dimensions not measured')
validation['aft_shape_revision']=dict(source='referentiefoto\'s echte opbouw (IMG_0297..0299)',flat_block_at_deck_height=True,stepped_cabinet_stair_and_aft_cabinets_removed=True,straight_U_back_wall_x=UX,U_corner_radius=C['U_corner_radius'],notch=dict(x=[S['notch_x'],nt],internal_y=[S['notch_y'],rheadinner],corner_radius=C['notch_corner_radius']),arm_inner_taper=dict(start_x=S['taper_x'],left_end_inner_y=S['left_end_inner'],right_end_inner_y=S['right_end_inner']),arm_end_radius=C['end_radius'],front_box_corner_radius=C['front_box_corner_radius'],detail_dimensions='notch, taper and radii from photo ratios or chosen by user; measured v17 dimensions unchanged')
validation['collisions']=[]
for i,(an,a,_,_) in enumerate(parts):
    ba=a.BoundingBox()
    for bn,b,_,_ in parts[i+1:]:
        bb=b.BoundingBox()
        if min(ba.xmax,bb.xmax)-max(ba.xmin,bb.xmin)<=.001 or min(ba.ymax,bb.ymax)-max(ba.ymin,bb.ymin)<=.001 or min(ba.zmax,bb.zmax)-max(ba.zmin,bb.zmin)<=.001:continue
        volume=a.intersect(b).Volume()
        if volume>.05:validation['collisions'].append(dict(a=an,b=bn,volume_mm3=round(volume,5)))
(ROOT/'controle.json').write_text(json.dumps(dict(validation=validation,parts=records),ensure_ascii=False,indent=2))
cq.exporters.export(assembly,str(ROOT/'STEP/SL109_v18_assemblage.step'))
with (ROOT/'onderdelen.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['onderdeel','aantal','X_mm','Y_mm','Z_mm','volume_cm3','printstand','in_assemblage','opmerking'])
    for r in records:w.writerow([r['part'],r['qty'],*r['print_mm'],r['volume_cm3'],r['orientation'],r['assembled'],r['note']])
assert not validation['collisions'],validation['collisions']
print('VALIDATED',len(records),'unique STL/STEP pairs; assembly',validation['assembly_size'],flush=True)
