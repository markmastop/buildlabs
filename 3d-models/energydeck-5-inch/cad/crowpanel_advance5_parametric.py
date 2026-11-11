"""CrowPanel Advance 5 ESP32-S3 enclosure, units mm. CadQuery >=2.6.
Run: python crowpanel_advance5_parametric.py [output_directory]
Print STLs are already oriented on Z=0. STEP assembly uses installed positions.
Designed around retained factory black plates; not the ESP32-P4 version.
"""
from pathlib import Path
import sys, math, json
import cadquery as cq
import trimesh

P = dict(panel_w=84.7, panel_h=136.4, clearance=0.5,
         case_w=100.0, case_h=182.0, tray_depth=24.0, lid_t=2.4,
         wall=2.4, corner_r=6.0, panel_bottom=40.0,
         window_w=79.4, window_h=122.8, window_x=-0.2475, window_y=106.9933,
         lean=15.0, foot_w=108.0, foot_d=80.0, foot_h=35.0,
         usb_x=0.0, usb_y=41.055, usb_z=12.705, straight=22.0,
         bend_r=10.0, cable_d=10.0, plug_w=20.0,
         pilot_d=2.6, clearance_d=3.4)
W,H,D,T=P['case_w'],P['case_h'],P['tray_depth'],P['lid_t']
wall=P['wall']; sy=[51.0,161.0]; sx=[-46.0,46.0]

def box(w,h,d,x=0,y=0,z=0):
    return cq.Workplane('XY').box(w,h,d,centered=(True,False,False)).translate((x,y,z))
def rr(w,h,r,z,d,x=0,y=0):
    return box(w,h,d,x,y,z).edges('|Z').fillet(r)
def cyl(r,h,x,y,z=0):
    return cq.Workplane('XY').center(x,y).circle(r).extrude(h).translate((0,0,z))
def installed(obj):
    return obj.mirror('XY').rotate((0,0,0),(1,0,0),90-P['lean']).translate((0,8,13))
# This is a reflection only for installation coordinates; exported parts keep normals valid.

def build():
    tray=rr(W,H,P['corner_r'],0,D)
    # Open electronics chamber: rear insertion, square-safe interior corners.
    cavity=rr(P['panel_w']+2*P['clearance'],P['panel_h']+2*P['clearance'],0.8,wall,D+2,y=P['panel_bottom']-P['clearance'])
    tray=tray.cut(cavity)
    window=rr(P['window_w'],P['window_h'],1.2,-1,wall+2,x=P['window_x'],y=P['window_y']-P['window_h']/2)
    tray=tray.cut(window)
    # Relieve the front screw heads (factory front screws protrude 1 mm).
    for x in [-37.15,37.15]:
        for y in [44,170]:
            tray=tray.cut(cyl(3.7,3,x,y,wall))
    # Hollow lower plinth, retaining 2.4 mm front and side walls.
    tray=tray.cut(rr(W-2*wall,37.1,3,wall,D+1,y=wall))
    # Reinstate a broad lower-edge support shelf, leaving USB plug passage.
    shelf=box(P['panel_w']+1,3.0,D-wall,y=37,z=wall)
    shelf=shelf.cut(box(P['plug_w'],5,D+1,x=P['usb_x'],y=36,z=wall))
    tray=tray.union(shelf)
    # Two rear screw pillars outside the device outline on each side.
    for x in sx:
        for y in sy:
            tray=tray.union(cyl(3.1,D-wall,x,y,wall))
            tray=tray.cut(cyl(P['pilot_d']/2,11,x,y,D-10))
    # Foot fastening receivers, blind holes, separated from electronics.
    for x in [-32,32]:
        tray=tray.union(box(10,13,D-wall,x=x,y=9,z=wall))
        tray=tray.cut(cyl(P['pilot_d']/2,13,x,15,D-12))
    # Cable guide: concave R10 centreline, 5 mm allowance, open to rear.
    # Inner radius 5 / outer radius 15 for a 10 mm channel; no forced sharp edge.
    uy,uz=P['usb_y']-P['straight'],P['usb_z']; R=P['bend_r']; a=P['cable_d']/2
    # Lower cradle surface follows the outside of the bend. Profile coordinates (local y, local z).
    path=[(uy+2,wall),(uy+2,uz-a),(uy,uz-a)]
    for i in range(1,25):
        q=math.pi/2*i/24
        path.append((uy-(R+a)*math.sin(q),uz+R-(R+a)*math.cos(q)))
    path += [(uy-R-a,D),(wall,D),(wall,wall)]
    guide=cq.Workplane('YZ',origin=(-P['cable_d']/2,0,0)).polyline(path).close().extrude(P['cable_d'])
    tray=tray.union(guide)
    # Rear lid: print outside down, no integral overhanging clips.
    lid=rr(W,H,P['corner_r'],0,T)
    for x in sx:
        for y in sy: lid=lid.cut(cyl(P['clearance_d']/2,T+2,x,y,-1))
    for x in [-32,32]: lid=lid.cut(cyl(P['clearance_d']/2,T+2,x,15,-1))
    # Ventilation low + high; 3 mm rounded slots, printed through the plate.
    for y in [56,62,154,160,166]:
        for x in [-24,-8,8,24]: lid=lid.cut(rr(11,3,1.45,-1,T+2,x=x,y=y))
    # Cable exit matches the end of the curved cradle.
    exit_y=uy-R
    lid=lid.cut(rr(12,12,3,-1,T+2,x=P['usb_x'],y=exit_y-6))
    # Lid inside faces tray at z=D; printed exterior stays on the print bed.
    lid_assembled=lid.mirror('XY').translate((0,0,D+T))
    # Stable tapered foot, no overhanging outside surfaces.
    bottom_wire=rr(P['foot_w'],P['foot_d'],6,0,1).faces('<Z').val().outerWire()
    top_wire=rr(102,44,6,P['foot_h'],1,y=8).faces('<Z').val().outerWire()
    foot=cq.Workplane('XY').add(bottom_wire).add(top_wire).toPending().loft()
    envelope=rr(W+0.7,H+1,6.3,-0.35,D+T+0.7,y=-0.35)
    foot=foot.cut(installed(envelope))
    # A rear-opening groove allows routing without passing the USB plug through a tunnel.
    # 12 mm wide; sloping floor, accessible from above, radiused vertical edges.
    cablecut=(cq.Workplane('YZ',origin=(-6,0,0)).polyline([(31,11),(85,0),(85,60),(31,60)]).close().extrude(12))
    foot=foot.cut(cablecut)
    # Rear access to two M3x16 screws: axis normal to display, holes begin at back of foot.
    for x in [-32,32]:
        bore=installed(cyl(1.7,100,x,15,0))
        recess=installed(cyl(3.4,100,x,15,D+T+3))
        foot=foot.cut(bore).cut(recess)
    # Rubber foot pockets 10 mm diameter, 0.6 deep, open to bed.
    for x in [-43,43]:
        for y in [10,69]: foot=foot.cut(cyl(5.1,0.7,x,y,-0.1))
    # Thin full-size test frame, same insertion opening and window.
    test=tray.intersect(box(W+2,H+2,5,y=-1,z=0))
    return dict(front=tray,back=lid,foot=foot,fit_test=test),lid_assembled

def main():
    out=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent);out.mkdir(parents=True,exist_ok=True)
    parts,lida=build();report={}
    for name,p in parts.items():
        assert p.val().isValid(),name
        assert len(p.solids().vals())==1,(name,len(p.solids().vals()))
        cq.exporters.export(p,str(out/f'crowpanel_{name}.stl'),tolerance=0.025,angularTolerance=0.08)
        cq.exporters.export(p,str(out/f'crowpanel_{name}.step'))
        mesh=trimesh.load_mesh(out/f'crowpanel_{name}.stl',process=True)
        assert mesh.is_watertight and mesh.is_winding_consistent,name
        report[name]=dict(dimensions_mm=mesh.extents.round(3).tolist(),solid_volume_mm3=round(p.val().Volume(),3),watertight=True)
    a=cq.Assembly(name='CrowPanel_Advance5_Stand')
    a.add(installed(parts['front']),name='front',color=cq.Color(0.12,0.13,0.14))
    a.add(installed(lida),name='back',color=cq.Color(0.17,0.18,0.19))
    a.add(parts['foot'],name='foot',color=cq.Color(0.12,0.13,0.14))
    a.save(str(out/'crowpanel_assembly.step'))
    (out/'dimensions.json').write_text(json.dumps(dict(parameters=P,parts=report),indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
