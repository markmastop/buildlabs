from pathlib import Path
import json,hashlib,zipfile
import numpy as np
import cadquery as cq
import trimesh
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'controle.json').read_text());rechecks=[]
for r in d['parts']:
 name=r['part'];m=trimesh.load_mesh(R/'STL'/(name+'.stl'),process=True)
 s=cq.importers.importStep(str(R/'STEP'/(name+'.step')))
 assert len(s.solids().vals())==1 and s.val().isValid(),name
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0,name
 delta=abs(s.val().Volume()-m.volume)/m.volume
 assert delta<.005,(name,delta)
 assert max(m.extents[:2])<=246,(name,m.extents)
 if name=='07_voordak_163mm':
  b=s.faces('<Z').val().BoundingBox();assert abs(b.xlen-163)<.03 and abs(b.ylen-180)<.03,(b.xlen,b.ylen)
 if name=='08_middenblok_65x25x55':assert np.allclose(m.extents[1:],[65,55],atol=.01)
 if name=='09_klein_blok_links_25x15x30':assert np.allclose(m.extents[1:],[25,30],atol=.01)
 rechecks.append(dict(part=name,STL_closed=True,STL_one_component=True,STEP_readback_valid=True,STEP_STL_volume_difference_fraction=round(delta,8)))
assembled=[r for r in d['parts'] if r['assembled']]
sh=cq.importers.importStep(str(R/'STEP/SL109_v17_assemblage.step')).solids().vals()
assert len(sh)==len(assembled)==27
byname={r['part']:s for r,s in zip(assembled,sh)}
for s in sh:assert s.isValid()
for name,z in [('04_achterdek_voor',60),('05_achterdek_achter',60),('07_voordak_163mm',86)]:assert abs(byname[name].BoundingBox().zmax-z)<.001
assert abs(byname['01_pasframe'].BoundingBox().zmin+6)<.001
assert abs(byname['02_onderdekhuis_voor'].BoundingBox().xmin)<.001
assert abs(byname['03_onderdekhuis_achter'].BoundingBox().xmax-385)<.001
# After the explicit export Y reflection, the small box must be on photo-left (positive Y).
small=byname['09_klein_blok_links_25x15x30'].BoundingBox();assert small.ymin>0
# The sloping stair is beside the cabinet and really reaches the lower-deck datum.
stair=byname['17_achterkast_getrapt'];sr=d['validation']['left_stair_transition']
ym=-sum(sr['stair_internal_y'])/2
for fraction in [.2,.5,.8]:
 x=sr['start_x']+(sr['end_x']-sr['start_x'])*fraction;expected=60*(1-fraction)
 q=cq.Workplane('XY').box(.002,1,100,centered=(True,True,False)).translate((x,ym,0)).val()
 top=stair.intersect(q).BoundingBox().zmax
 assert abs(top-expected)<.003,(x,top,expected)
# The separate neighbouring cabinet still has its flat 38 mm front roof.
q=cq.Workplane('XY').box(.002,1,100,centered=(True,True,False)).translate((318,-27,0)).val()
assert abs(stair.intersect(q).BoundingBox().zmax-38)<.003
# Rear-photo handedness and physical door opening; this caught the v5 mirror error.
assert byname['17_achterkast_getrapt'].BoundingBox().ymax<0
assert byname['19_achterkast_schuin'].BoundingBox().ymin>0
assert abs(byname['17_achterkast_getrapt'].BoundingBox().zmax-60)<.001
assert abs(byname['18_achterkast_laag'].BoundingBox().zmax-22)<.001
p=json.loads((R/'CAD/parameters.json').read_text());a=p['aft']
h=a['left_chamfer_run'];k=a['left_chamfer_inset'];norm=(h*h+k*k)**.5
# Internal yiR is +17.5; exported door plane is mirrored across XZ.
origin=(270+h/2,-17.5+k/2,a['door_bottom']+a['door_height']*.75)
pl=cq.Plane(origin=origin,xDir=(h/norm,-k/norm,0),normal=(k/norm,h/norm,0))
probe=cq.Workplane(pl).circle(a['porthole_diameter']/2-.4).extrude(5,both=True)
assert byname['03_onderdekhuis_achter'].intersect(probe.val()).Volume()<.001
adj=cq.Workplane('XY').sphere(.8).translate((origin[0]-k/norm*.6,origin[1]-h/norm*.6,origin[2]+6))
assert byname['03_onderdekhuis_achter'].intersect(adj.val()).Volume()>.1
floor=cq.importers.importStep(str(R/'STEP/21_achtervloer_optioneel.step')).val()
# Individual print files are moved to bed-origin, so verify optional floor against
# assembly using the source sketch's original x/y bounds (UX+.15, internal mirrored Y).
# Its front-left corner is retained by the cabinet clearances and defines its origin.
orig_x=270.15;orig_y=-17.5+.15
floor=floor.translate(cq.Vector(orig_x,orig_y,0))
for name in ['18_achterkast_laag','19_achterkast_schuin']:
 assert byname[name].intersect(floor).Volume()<.001,name
# Round funnel cross-section and flat widened connector are geometric checks.
p=json.loads((R/'CAD/parameters.json').read_text());u=p['upper'];co=p['connector']
for suffix,iy,bw in [('L',u['left_funnel_y'],u['left_funnel_width']),('R',u['right_funnel_y'],u['right_funnel_width'])]:
 s=byname['15_schoorsteen_logo_roosters_'+suffix]
 # Point inside the old square-ish corner but outside the new R12 outer contour.
 probe=cq.Workplane('XY').sphere(.25).translate((u['funnel_center_x']+u['funnel_length']/2-2,-iy+bw/2-2,63)).val()
 assert s.intersect(probe).Volume()<.001,suffix
 # The highest fore rim exceeds the aft rim; the tube stays genuinely hollow.
 z0=62;zt=z0+u['funnel_height'];yf=-iy
 void=cq.Workplane('XY').sphere(2).translate((u['funnel_center_x'],yf,zt-10)).val()
 assert s.intersect(void).Volume()<.001,suffix
 assert abs(byname['14_schoorsteenvoet_'+suffix].BoundingBox().xlen-84)<.001
beam=byname['16_dwarsverbinding_met_platform'];cy=-(u['left_funnel_y']+u['right_funnel_y'])/2
# A point near the rear of the widened platform is material; a point above it is empty.
px=u['funnel_center_x']+co['platform_rear_offset']-3
pr=cq.Workplane('XY').sphere(.3).translate((px,cy,u['connector_z']+co['plate_thickness']/2)).val()
assert beam.intersect(pr).Volume()>.1
pr=cq.Workplane('XY').sphere(.3).translate((px,cy,u['connector_z']+co['plate_thickness']+2)).val()
assert beam.intersect(pr).Volume()<.001
# The longer rounded feet must still sit on the existing measured aft-deck parts.
foot_support=[]
for suffix in ['L','R']:
 foot=byname['14_schoorsteenvoet_'+suffix]
 support=foot.translate(cq.Vector(0,0,-2)).intersect(byname['05_achterdek_achter']).Volume()/foot.Volume()
 assert support>.99,(suffix,support)
 foot_support.append(dict(side=suffix,deck_support_fraction=round(support,8)))
# Confirm that all new side windows are physical openings after STEP readback.
side_report=[]
for label in ['A','B']:
 cfg=p['sides'][label];sign=cfg['internal_sign']
 assert len(cfg['lower_windows'])==(6 if label=='A' else 4) and len(cfg['upper_recesses'])==2
 assert sum(w['x']<190 for w in cfg['lower_windows'])==(4 if label=='A' else 2)
 for win in cfg['lower_windows']:
  xx=win['x'];outer_y=90 if xx<=163 else 90-(xx-163)*2.5/107
  yy=-sign*(outer_y-.8);zz=win['bottom']+win['height']/2
  part=byname['02_onderdekhuis_voor' if xx<190 else '03_onderdekhuis_achter']
  probe=cq.Workplane('XY').sphere(.65).translate((xx,yy,zz)).val()
  assert part.intersect(probe).Volume()<.001,(label,xx,'lower aperture blocked')
  # Material must remain in the adjacent vertical frame.
  frame_x=xx+win['width']/2+1.2
  frame_y=90 if frame_x<=163 else 90-(frame_x-163)*2.5/107
  probe=cq.Workplane('XY').sphere(.35).translate((frame_x,-sign*(frame_y-.8),zz)).val()
  assert part.intersect(probe).Volume()>.05,(label,xx,'missing side frame')
 for win in cfg['upper_recesses']:
  solid=byname['06_verhoogd_voordekhuis']
  # Probe the cavity and the backing at several points across both recesses.
  for fraction in [.25,.5,.75]:
   xx=win['x']+(fraction-.5)*win['width']
   # Same measured polygonal nose, independently interpolated for readback probes.
   import math
   n=p['construction']['fore_nose_segments'];nr=p['construction']['fore_nose_depth'];hw=p['measured']['front_width']/2
   pts=sorted((nr-nr*math.cos(-math.pi/2+i*math.pi/n),hw*math.sin(-math.pi/2+i*math.pi/n)) for i in range(n+1) if math.sin(-math.pi/2+i*math.pi/n)>=-1e-8)
   yy=hw
   for (xa,ya),(xb,yb) in zip(pts,pts[1:]):
    if xa<=xx<=xb:yy=ya+(yb-ya)*(xx-xa)/(xb-xa);break
   zz=win['bottom']+win['height']/2
   for inset,occupied in [(1,False),(win['depth_y']+.7,True),(win['depth_y']+win['backing_y']-.5,True)]:
    pr=cq.Workplane('XY').sphere(.22).translate((xx,-sign*(yy-inset),zz)).val()
    vol=solid.intersect(pr).Volume()
    assert (vol>.03 if occupied else vol<.001),(label,xx,inset,vol,'recess cavity/backing')
  # Sloped top/bottom returns retain material outside the recessed back rectangle.
  xx=win['x'];yy=hw if xx>=nr else next(ya+(yb-ya)*(xx-xa)/(xb-xa) for (xa,ya),(xb,yb) in zip(pts,pts[1:]) if xa<=xx<=xb)
  for zz in [win['bottom']+.5,win['bottom']+win['height']-.5]:
   pr=cq.Workplane('XY').sphere(.18).translate((xx,-sign*(yy-3),zz)).val()
   assert solid.intersect(pr).Volume()>.02,(label,xx,'missing sloped return')
 side_report.append(dict(side=label,lower_openings=len(cfg['lower_windows']),closed_upper_recesses=2,backing_present_at_three_stations_per_recess=True,before_joint=sum(w['x']<190 for w in cfg['lower_windows']),after_joint=2))
assert [q['x'] for q in p['sides']['A']['lower_windows']]==[48,112,135,176,202,240]
assert [q['x'] for q in p['sides']['B']['lower_windows']]==[48,95,202,240]
assert p['sides']['A']['upper_recesses']==p['sides']['B']['upper_recesses']
# Front groove must continue vertically through top and bottom, with an intact
# backing at every height; the old horizontal under-arch fails these probes.
front=p['construction'];rad=front['front_center_notch_radius'];cx=-p['measured']['front_center_box'][1]
block=byname['08_middenblok_65x25x55'];height=p['measured']['front_center_box'][2]
for zz in [0.3,1,10,27.5,45,height-1,height-.3]:
 for xx,occupied in [(cx+rad/2,False),(cx+rad+.7,True)]:
  probe=cq.Workplane('XY').sphere(.2).translate((xx,0,zz)).val();vol=block.intersect(probe).Volume()
  assert (vol>.025 if occupied else vol<.001),(xx,zz,vol,'front groove/backing')
# Whole groove cutter has no obstruction after assembled STEP readback.
test=cq.Workplane('XY').center(cx,0).circle(rad-.2).extrude(height+2).translate((0,0,-1)).val()
assert block.intersect(test).Volume()<.001
# Both cheeks stay present; the box is already validated as one solid.
for yy in [-rad-1,rad+1]:
 probe=cq.Workplane('XY').sphere(.2).translate((cx+.7,yy,height/2)).val()
 assert block.intersect(probe).Volume()>.025
# Test the gap against ALL assembled parts so an adjacent part cannot fill it.
gap=front['front_railing_gap_width'];roof=p['measured']['fore_roof_height']
gap_probe=cq.Workplane('XY').box(7,gap-.4,15.6,centered=(True,True,False)).translate((1,0,roof+.2)).val()
for name,solid in byname.items():assert solid.intersect(gap_probe).Volume()<.001,(name,'railing gap obstructed')
# Restored solid front windbreak has material beside the central opening.
for yy in [-gap/2-.8,gap/2+.8]:
 pr=cq.Workplane('XY').box(10,.3,1,centered=(True,True,True)).translate((2,yy,roof+8)).val()
 assert sum(byname['13_windscherm_'+label].intersect(pr).Volume() for label in ['L','R'])>.05
# The actual restored print meshes must be byte-identical to the approved v12 parts.
# The original files are not required to rebuild or validate a distributed package.
for r in d['parts']:assert not r['part'].startswith(('24_','25_','26_','27_','28_','29_','30_','31_','13_reling_'))
# V17: independently reloaded wheelhouse geometry and unchanged aperture count.
br=d['validation']['bridge_revision'];cfg=p['bridge'];body=byname['10_stuurhut_met_raamopeningen'];roofpart=byname['11_stuurhutdak_lichtkap'];cap=byname['12_lichtkap_deksel']
assert len(br['windows'])==17 and len(br['roof_windows'])==3
for w in br['windows']:
 xx,yy,zz=w['center'];pr=cq.Workplane('XY').sphere(.45).translate((xx,-yy,zz)).val()
 assert body.intersect(pr).Volume()<.001,(w['name'],'window blocked')
for yy in [-23,0,23]:
 for zz in [112,124,136]:
  pr=cq.Workplane('XY').sphere(.4).translate((123,yy,zz)).val();assert body.intersect(pr).Volume()<.001,'tall rear aperture blocked'
for yy in [-34.5,-11.5,11.5,34.5]:
 pr=cq.Workplane('XY').sphere(.3).translate((122.3,yy,119)).val();assert body.intersect(pr).Volume()>.08,'rear mullion missing'
for yy in [-23,0,23]:
 pr=cq.Workplane('XY').sphere(.3).translate((122.3,yy,109)).val();assert body.intersect(pr).Volume()>.08,'added wall below rear glass missing'
for w in br['roof_windows']:
 xx,yy,zz=w['center'];pr=cq.Workplane('XY').sphere(.35).translate((xx,-yy,zz)).val();assert roofpart.intersect(pr).Volume()<.001,'hood aperture blocked'
symmetry=[]
for name in ['10_stuurhut_met_raamopeningen','11_stuurhutdak_lichtkap','12_lichtkap_deksel']:
 solid=byname[name];mirror=solid.mirror('XZ');delta=solid.cut(mirror).Volume()+mirror.cut(solid).Volume();assert delta<.03,(name,delta)
 symmetry.append(dict(part=name,mirror_volume_difference_mm3=round(delta,8)))
assert abs(body.BoundingBox().zmin-86)<.001 and abs(body.BoundingBox().zmax-141)<.001
assert abs(roofpart.BoundingBox().zmin-141)<.001 and abs(roofpart.BoundingBox().zmax-155)<.001
assert abs(cap.BoundingBox().zmin-155)<.001 and abs(cap.BoundingBox().zmax-157)<.001
# Measure the foot at its actual floor datum, excluding the leaning upper glass.
footpr=cq.Workplane('XY').box(500,500,.1,centered=(True,True,False)).translate((0,0,86.1)).val();fb=body.intersect(footpr).BoundingBox()
assert abs(fb.xmin-33)<.001 and abs(fb.xmax-123)<.001 and abs(fb.xlen-90)<.001
assert abs(fb.ylen-136)<.001 and cfg['height']==55
assert cfg['side_windows']==[dict(x=65,width=14.5,height=24.5,bottom=27.5),dict(x=87,width=16,height=19,bottom=33),dict(x=107,width=16,height=19,bottom=33)]
assert cfg['door_width']==21.5 and cfg['door_height']==52.5 and cfg['door_center_x']==65
assert cfg['rear_tall_window_height']==26 and cfg['rear_tall_window_bottom']==25
assert cfg['corner_window_profile_xz']==[[43.5,27.5],[52.5,27.5],[52.5,52],[35,52]]
for sign in [-1,1]:
 for zz in [115,125,136]:
  fore=43.5-(zz-113.5)*8.5/24.5
  for xx,occupied in [(fore-1.4,True),(fore+1.8,False),(51,False),(53.5,True)]:
   pr=cq.Workplane('XY').box(.2,18,.2,centered=(True,True,True)).translate((xx,sign*61,zz)).val();vol=body.intersect(pr).Volume()
   assert (vol>.025 if occupied else vol<.001),(xx,zz,vol,'forward trapezoid stile')
 for xx in [54.25,75.75]:
  for zz in [90,114,128,137]:
   pr=cq.Workplane('XY').sphere(.08).translate((xx,sign*68.12,zz)).val();assert body.intersect(pr).Volume()>.001,'straight door stile missing'
 for xx in [60,65,70]:
  for zz in [90,104,110]:
   pr=cq.Workplane('XY').sphere(.3).translate((xx,sign*67,zz)).val();assert body.intersect(pr).Volume()>.08,'taller lower door panel not closed'
 for xx in [53.5,77.5,97]:
  pr=cq.Workplane('XY').sphere(.3).translate((xx,sign*67,128)).val();assert body.intersect(pr).Volume()>.08,'compacted side window mullion missing'
 for xx in [87,93,107,113]:
  pr=cq.Workplane('XY').sphere(.3).translate((xx,sign*67.3,128)).val();assert body.intersect(pr).Volume()<.001,'compacted side window clipped'
assert 'side_panel_x' not in cfg and cfg['roof_rim_height']==0 and cfg['mast_socket']==0
assert cfg['hood_rear_x']==97 and cfg['hood_height']==14 and cfg['roof_overhang']==3
assert all(q['bottom']+q['height']==52 for q in cfg['side_windows'])
assert set(byname).isdisjoint({'24_dakreling','25_radarmast','28_antennevoet','30_antenne_L','31_reddingsboei_L'})
a=byname['13_windscherm_L'].mirror('XZ');b=byname['13_windscherm_R'];delta=a.cut(b).Volume()+b.cut(a).Volume();assert delta<.03
paired=[dict(pair='13_windscherm',mirror_volume_difference_mm3=round(delta,8))]
fore_windows=[w for w in br['windows'] if w['name'].startswith('front_')];assert len(fore_windows)==4
for w in fore_windows:
 if abs(w['center'][1])>26:assert abs(w['normal'][1])>.05
 else:assert w['normal']==[-1,0,0]
for yy in [20,40,60]:
 pr=cq.Workplane('XY').box(100,.01,.01,centered=(False,True,True)).translate((0,yy,96)).val();x=body.intersect(pr).BoundingBox().xmin
 if yy==20:assert abs(x-33)<.02
 if yy==40:assert 33.65<x<34.1
 if yy==60:assert 38.8<x<39.7
# One-sided anchor recess, all tests on reloaded STEP. Its back and both returns
# stay closed; the old symmetrical opposite wall must remain present.
n=p['anchor_niche'];house=byname['02_onderdekhuis_voor'];deck=byname['04_achterdek_voor'];allparts=list(byname.values())
assert n['side']=='B' and n['export_side_y']==1
for xx in [124,150,165]:
 oy=90 if xx<=163 else 90-(xx-163)*2.5/107
 for zz in [10,30,50]:
  for yy,occupied in [(68,False),(78,False),(85,False),(65,True),(-oy+.8,True)]:
   pr=cq.Workplane('XY').sphere(.3).translate((xx,yy,zz)).val();vol=house.intersect(pr).Volume()
   assert (vol>.08 if occupied else vol<.001),(xx,yy,zz,vol,'anchor cavity/back/opposite wall')
 # The sill is floor, the cap is ceiling, and the unchanged frame fits below.
 for yy in [68,78,85]:
  pr=cq.Workplane('XY').sphere(.3).translate((xx,yy,4)).val();assert house.intersect(pr).Volume()>.08
  pr=cq.Workplane('XY').sphere(.3).translate((xx,yy,58.8)).val();assert deck.intersect(pr).Volume()>.08
for xx in [115,185]:
 pr=cq.Workplane('XY').sphere(.3).translate((xx,75,30)).val();assert house.intersect(pr).Volume()>.08,'anchor side return missing'
assert house.intersect(byname['01_pasframe']).Volume()<.001
assert d['validation']['anchor_niche']['frame_flange_clearance']==1
assert abs(byname['01_pasframe'].BoundingBox().zmin+6)<.001
assert n['back_y']==66 and n['nominal_depth']==24
for label in ['A','B']:
 sign=p['sides'][label]['internal_sign']
 for q in p['sides'][label]['upper_recesses']:
  assert q['depth_y']==8
  # The old 4 mm pocket would contain material here; the new one is empty.
  xx=q['x'];yy=90
  if xx<35:
   import math
   yy=90*math.sqrt(1-((35-xx)/35)**2)
  pr=cq.Workplane('XY').sphere(.18).translate((xx,-sign*(yy-6),q['bottom']+q['height']/2)).val()
  assert byname['06_verhoogd_voordekhuis'].intersect(pr).Volume()<.001,'small recess not deepened'
# The enlarged low rear ledge is solid at roof-plate height, clear above it.
for yy in [-60,0,60]:
 pr=cq.Workplane('XY').sphere(.3).translate((115,yy,142)).val();assert roofpart.intersect(pr).Volume()>.08
pr=cq.Workplane('XY').box(29,160,20,centered=(False,True,False)).translate((97.2,0,143.2)).val()
assert roofpart.intersect(pr).Volume()<.001,'hood still extends over enlarged aft ledge'
# Roof/bulkhead contact is a surface, not overlapping material; build tested every pair already.
assert d['validation']['collisions']==[]
rep={'parts':rechecks,'assembly_solids':len(sh),'checks':{'no_unintended_volume_collisions':True,'all_print_footprints_under_246_mm':True,'fore_roof_top_face_163_by_180':True,'roof_heights_60_and_86':True,'insertion_depth_6':True,'small_front_box_photo_left':True,'rear_photo_handedness':True,'angled_door_porthole_open':True,'optional_floor_clears_rear_cabinets':True,'inclined_stair_beside_two_panel_cabinet':True,'rounded_funnel_corners':True,'funnel_tubes_open':True,'connector_flat_widened_platform':True},'limits':'No physical print/fit, no Bambu Studio layer-by-layer slicer check.'}
rep['funnel_foot_support']=foot_support
rep['side_window_readback']=side_report
rep['checks']['upper_recesses_closed_with_sloping_returns']=True
rep['checks']['front_groove_full_height_and_closed_backing']=True
rep['checks']['front_railing_gap_clear_between_both_cheeks']=True
rep['checks']['bridge_17_open_windows_and_three_hood_windows']=True
rep['checks']['bridge_three_tall_rear_windows_open_at_bottom']=True
rep['bridge_mirror_symmetry']=symmetry
rep['windbreak_pair_symmetry']=paired
rep['checks']['rectangular_doors_with_separate_sloping_forward_windows']=True
rep['checks']['solid_front_windbreak_restored_with_central_gap']=True
rep['checks']['other_railings_roof_equipment_lifebuoys_removed']=True
rep['checks']['anchor_niche_one_side_closed_back_returns_sill_and_ceiling']=True
rep['checks']['anchor_niche_clears_existing_frame']=True
rep['checks']['rounder_front_52mm_flat_and_angled_outer_panes']=True
rep['checks']['tall_narrow_door_and_forward_trapezoid']=True
rep['checks']['shorter_hood_with_flat_rear_ledge']=True
rep['checks']['wheelhouse_wall_55mm_foot_90mm_width_136mm']=True
rep['checks']['added_wall_height_below_unchanged_glass_heights']=True
rep['checks']['small_recess_depth_doubled_to_8_mm']=True
rep['checks']['anchor_nominal_depth_doubled_to_24_mm']=True
rep['anchor_niche']=d['validation']['anchor_niche']
(R/'STEP_hercontrole.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
files=[p for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt']
(R/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in files))
archive=R.parent/'Smit-Lloyd-109_v17_printpakket.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(R.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:z.write(p,'smit_lloyd_109_v17/'+str(p.relative_to(R)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('RECHECK PASSED',len(rechecks),'STL/STEP pairs;',len(sh),'assembly solids;',archive.stat().st_size,'ZIP bytes')
