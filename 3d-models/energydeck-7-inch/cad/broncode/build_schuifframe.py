"""CrowPanel Advance 7, v6.1: uitsluitend de bodem onder de USB-ruimte gesloten.
Python 3.11+, cadquery 2.8.0, numpy, Pillow. Includes front retaining frame.
"""
from pathlib import Path
import math,json
import cadquery as cq
from PIL import Image,ImageDraw
from cad_common import mesh_report,font,render_panel

SOURCE_DIR=Path(__file__).resolve().parent
OUT=(SOURCE_DIR.parent if SOURCE_DIR.name=='broncode' else
     SOURCE_DIR.parent/'outputs'/'CrowPanel7_schuifframe_v6_bodem_dicht')
OUT.mkdir(parents=True,exist_ok=True)
ANGLE=18.0
SW=108.36; SH=181.26
CLEAR=.6
SUPPORT_HEIGHT=10.0         # User-specified, measured from the existing floor.
PLUG_PROJECTION=9.0        # Inferred from user's 10 mm support / 1 mm clearance.
FLOOR_V=-CLEAR
LIFT=FLOOR_V+SUPPORT_HEIGHT # Screen bottom shifts from v=0 to v=9.4.
WALL=3.4
OW=SW+2*CLEAR+2*WALL
V0=-9.; V1=SH+9.+LIFT
FRONT=-16.2; REAR=3.2; BEZEL_T=2.4
RY=-25.; RZ=36.
S=math.sin(math.radians(ANGLE)); C=math.cos(math.radians(ANGLE))
RAIL_V=[-4.5,SH+4.5+LIFT]
FRAME_REAR=FRONT-.2
RAIL_START=-55.0
RAIL_END=51.3
RAIL_NECK=.8
RAIL_HEAD=2.0
RAIL_FLARE=1.2
RAIL_DEPTH=2.4
SLIDE_CLEAR=.25
PIN_X=52.6
PIN_V=RAIL_V[1]
PIN_SHOULDER=-12.5
SUPPORT_RANGES=[(-42.5,-17.5),(17.5,42.5)]
SUPPORT_BACK=-.2
SUPPORT_FRONT=-15.2
SUPPORT_TOP=LIFT
USB_WIDTH=30.0
USB_FRONT=-14.2             # 2.0 mm front web; v4 left a 3.7 mm web.
USB_TOP=LIFT+11.0
USB_AXIS_W=1.605-8.0       # Actual socket mouth from manufacturer STEP.
USB_MOUTH_V=LIFT+179.06-176.8942
ADAPTER_FRONT=-13.2        # Conservative allowance, NOT a measured plug.

def support_bars():
 # Tops are exactly 10 mm above the existing floor at v=-0.6.
 # Embedded roots fuse to that floor. The screen sits 9.4 mm higher than
 # v2, and the complete case, bezel, top fasteners and ports follow it.
 bars=[sb(x0,x1,-2.5,SUPPORT_TOP,SUPPORT_FRONT,SUPPORT_BACK) for x0,x1 in SUPPORT_RANGES]
 return bars

def yz(v,w): return (RY+v*S+w*C,RZ+v*C-w*S)
def block(dx,dy,dz,cx,cy,z0):
 return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,False)).translate((cx,cy,z0))
def profile(points,xmin,width):
 return cq.Workplane('YZ').polyline(points).close().extrude(width).translate((xmin,0,0))
def sb(x0,x1,v0,v1,w0,w1):
 return profile([yz(v0,w0),yz(v1,w0),yz(v1,w1),yz(v0,w1)],x0,x1-x0)
def local_plane(w):
 y,z=yz(0,w)
 # Reversed local X gives a right-handed plane with local Y along screen-v.
 # All local X features are symmetric about zero.
 return cq.Plane(origin=(0,y,z),xDir=(-1,0,0),normal=(0,C,-S))
def rect_solid(width,v0,v1,w0,w1,radius=0):
 # Workplane y axis runs in the positive screen-v direction.
 a=cq.Workplane(local_plane(w0)).center(0,(v0+v1)/2).rect(width,v1-v0).extrude(w1-w0)
 if radius:
  edges=[e for e in a.edges().vals() if e.geomType()=='LINE' and abs(e.Length()-(w1-w0))<1e-5]
  a=a.newObject(edges).fillet(radius)
 return a
def hole(x,v,w0,w1,r):
 return cq.Workplane(local_plane(w0)).center(x,v).circle(r).extrude(w1-w0)
def rail(x0,x1,v,female=False,lead=True):
 # A 45-degree flared neck prints face-down without rail supports. The
 # parallel rear flange gives 0.25 mm of normal and lateral running clearance.
 if female:
  n=RAIL_NECK+SLIDE_CLEAR; h=RAIL_HEAD+SLIDE_CLEAR
  points=[(v-n,FRONT-.5),(v+n,FRONT-.5),(v+n,FRONT),
          (v+h,FRONT+RAIL_FLARE),(v+h,FRONT+RAIL_DEPTH+.3),
          (v-h,FRONT+RAIL_DEPTH+.3),(v-h,FRONT+RAIL_FLARE),(v-n,FRONT)]
 else:
  n=RAIL_NECK; h=RAIL_HEAD
  points=[(v-n,FRAME_REAR-.05),(v+n,FRAME_REAR-.05),(v+n,FRONT),
          (v+h,FRONT+RAIL_FLARE),(v+h,FRONT+RAIL_DEPTH),
          (v-h,FRONT+RAIL_DEPTH),(v-h,FRONT+RAIL_FLARE),(v-n,FRONT)]
 p=profile([yz(vv,ww) for vv,ww in points],x0,x1-x0)
 if not female and lead:
  p=p.faces('<X').edges().chamfer(.3)
 return p

def clip_port():
 shaft=sb(PIN_X-1.3,PIN_X+1.3,PIN_V-2.2,PIN_V+2.2,PIN_SHOULDER,REAR+1)
 detent=sb(PIN_X-1.3,PIN_X+1.3,PIN_V-2.65,PIN_V+2.65,-15.5,PIN_SHOULDER+.01)
 return shaft.union(detent)

def build_clip():
 # Two 1 mm spring legs flex about 0.2 mm each during insertion/removal.
 # The rear cap is flush with one X face so both legs print flat on the bed.
 clip=None
 upper=[(-15.2,.9),(-15.2,1.6),(-14.4,2.4),(-13.2,2.4),
        (-12.6,1.9),(REAR+.1,1.9),(REAR+.1,.9)]
 for side in [-1,1]:
  p=profile([yz(PIN_V+side*dv,w) for w,dv in upper],PIN_X-1,2)
  clip=p if clip is None else clip.union(p)
 cap=sb(PIN_X-1,PIN_X+4.5,PIN_V-2.3,PIN_V+2.3,REAR,REAR+2)
 cap=cap.edges('|X').fillet(.6)
 return clip.union(cap).clean()

def body_ring():
 shell=rect_solid(OW,V0,V1,FRONT,REAR,4.5)
 # Front loading: interior is completely open before the bezel is attached.
 cavity=rect_solid(SW+2*CLEAR,FLOOR_V,SH+CLEAR+LIFT,FRONT-2,0,2.0)
 shell=shell.cut(cavity)
 # Preserve the original acrylic back: broad access opening for plugs/buttons.
 rear_open=rect_solid(104,7+LIFT,SH-3+LIFT,-.1,REAR+1,3.0)
 shell=shell.cut(rear_open)
 # Close only the missing floor below the USB pocket, at the original floor
 # datum. USB/module are loaded through the open front before fitting the
 # sliding frame. Everything above the floor, including the rear outlet,
 # stays unchanged. The rail cuts below are applied exactly as before.
 slot=sb(-USB_WIDTH/2,USB_WIDTH/2,FLOOR_V,USB_TOP,USB_FRONT,REAR+1)
 shell=shell.cut(slot)
 for bar in support_bars():
  shell=shell.union(bar)
 # Closed left end acts as a hard stop; the rails enter from the right.
 for v in RAIL_V:
  shell=shell.cut(rail(RAIL_START,OW/2+1,v,female=True))
 shell=shell.cut(clip_port())
 return shell.clean()

def build_main():
 base=block(126,120,6,0,0,0).edges('|Z').fillet(8).edges('#Z').fillet(.65)
 # Slim, fixed cheeks join the rear perimeter, leaving the ports uncovered.
 outline=[(-40,5.5),(51,5.5),yz(114,8),yz(114,3.05),yz(-9,3.05)]
 aperture=[(-10,40),(11,108),(35,16)]
 for x in [-59.5,52.5]:
  cheek=profile(outline,x,7)
  cheek=cheek.cut(profile(aperture,x-1,9))
  base=base.union(cheek)
 base=base.union(body_ring())
 base=base.cut(block(15,124,6,0,0,3.2))
 for x in [-48,48]:
  for y in [-44,44]:
   base=base.cut(cq.Workplane('XY').center(x,y).circle(6.2).extrude(1.1))
 return base.clean()

def build_bezel():
 # Uniform bezel is proud of the glass; no transparent overlay over touch area.
 ring=rect_solid(OW,V0,V1,FRAME_REAR-BEZEL_T,FRAME_REAR,4.5)
 window=rect_solid(93,10.5+LIFT,SH-10.5+LIFT,FRAME_REAR-BEZEL_T-1,FRONT+1,3.0)
 ring=ring.cut(window)
 ring=ring.union(rail(RAIL_START,RAIL_END,RAIL_V[1]))
 # The final bottom rail has a 36 mm gap around the USB adapter path.
 for x0,x1 in [(RAIL_START,-18),(18,RAIL_END)]:
  ring=ring.union(rail(x0,x1,RAIL_V[0]))
 return ring.clean()

def flat(part):
 # Rear face on the bed. Screen-v becomes +Y, front-w becomes +Z.
 p=part.rotate((0,0,0),(1,0,0),ANGLE-90)
 b=p.val().BoundingBox()
 return p.translate((-b.xmin,-b.ymin,-b.zmin))

def flat_front(part):
 # Visible face on the bed, rail flanges upward.
 p=part.rotate((0,0,0),(1,0,0),ANGLE+90)
 b=p.val().BoundingBox()
 return p.translate((-b.xmin,-b.ymin,-b.zmin))

def flat_clip(part):
 # Both spring legs lie flat; layer lines follow their length.
 p=part.rotate((0,0,0),(0,1,0),-90)
 b=p.val().BoundingBox()
 return p.translate((-b.xmin,-b.ymin,-b.zmin))

def build_coupon():
 # Actual bottom portion of the case, including both support bars and USB.
 region=sb(-OW/2-1,OW/2+1,V0-1,13+LIFT,FRONT-4,REAR+1)
 return body_ring().intersect(region).clean()

def build_slide_coupons():
 region=sb(-30,-8,RAIL_V[1]-4.5,RAIL_V[1]+4.5,FRAME_REAR-BEZEL_T-1,REAR+1)
 return body_ring().intersect(region).clean(),build_bezel().intersect(region).clean()

def build_clip_coupon():
 region=sb(PIN_X-3,PIN_X+5,PIN_V-4.5,PIN_V+4.5,FRONT-1,REAR+1)
 return body_ring().intersect(region).clean()

def main():
 main=build_main(); bezel=build_bezel(); coupon=build_coupon(); clip=build_clip()
 test_case,test_frame=build_slide_coupons()
 reports=[]
 for name,p in [('00a_pasproef_schuif_case',flat(test_case)),('00b_pasproef_schuif_frame',flat_front(test_frame)),('00c_pasproef_borgclip_case',flat(build_clip_coupon())),('01_pasproef_USB_10mm',flat(coupon)),('02_case_schuifframe',main),('03_voorframe_schuif',flat_front(bezel)),('04_borgclip',flat_clip(clip))]:
  cq.exporters.export(p,str(OUT/(name+'.stl')),tolerance=.04,angularTolerance=.12)
  cq.exporters.export(p,str(OUT/(name+'.step')))
  reports.append(mesh_report(OUT/(name+'.stl'),p))
 asm=cq.Assembly(name='CrowPanel7_beschermde_houder')
 asm.add(main,name='Houder_en_behuizing',color=cq.Color(.2,.25,.25))
 asm.add(bezel,name='Voorframe',color=cq.Color(.15,.2,.2))
 asm.add(clip,name='Uitneembare_borgclip',color=cq.Color(.8,.5,.16))
 asm.save(str(OUT/'05_assemblage.step'))
 main.val().exportBrep(str(OUT/'main_check.brep'))
 bezel.val().exportBrep(str(OUT/'bezel_check.brep'))
 clip.val().exportBrep(str(OUT/'clip_check.brep'))
 (OUT/'modelcontrole.json').write_text(json.dumps(reports,indent=2))
 print(json.dumps(reports,indent=2),flush=True)
 preview(main,bezel,clip)
 support_preview(coupon)
 slide_preview(test_case,test_frame,clip)

def support_preview(coupon):
 # Colour marks the two real, nominal-height contact areas, not a raised
 # or exaggerated shape. Geometry is taken from the final model.
 marked=[sb(a,b,SUPPORT_TOP-.03,SUPPORT_TOP+.02,SUPPORT_FRONT,SUPPORT_BACK) for a,b in SUPPORT_RANGES]
 tray=render_panel([(coupon,(177,183,181))]+[(x,(231,143,43)) for x in marked],[.8,-1.2,1.7],(1500,790))
 sheet=Image.new('RGB',(1640,1090),(244,244,240)); d=ImageDraw.Draw(sheet)
 d.text((70,35),'Twee geïntegreerde steunbalkjes van 10 mm',font=font(43,True),fill=(29,42,44))
 d.text((73,103),'Gelijke hoogte links en rechts; de stekker blijft in het midden vrij.',font=font(27),fill=(84,94,94))
 sheet.paste(tray,(70,177)); d=ImageDraw.Draw(sheet)
 d.text((73,978),'Oranje = contactvlakken. Middenruimte tussen balkjes: 35 mm.',font=font(26),fill=(29,42,44))
 d.text((73,1025),'10 mm boven de bodem: bij 9 mm stekkeruitsteek blijft 1 mm vrij. USB-doorgang: 30 mm breed.',font=font(22),fill=(84,94,94))
 sheet.save(OUT/'Steunbalkjes_detail.png')

def slide_preview(test_case,test_frame,clip):
 region=sb(-20.2,-19.8,RAIL_V[1]-5,RAIL_V[1]+5,FRAME_REAR-BEZEL_T-1,REAR+1)
 section_case=test_case.intersect(region)
 section_frame=test_frame.intersect(region)
 first=render_panel([(section_case,(177,183,181)),(section_frame,(49,100,109))],[1,.05,.12],(950,620))
 second=render_panel([(clip,(205,130,52))],[1,.15,.2],(950,620))
 sheet=Image.new('RGB',(2000,940),(244,244,240)); d=ImageDraw.Draw(sheet)
 d.text((65,35),'Schuifframe met verborgen geleiding',font=font(46,True),fill=(29,42,44))
 d.text((68,112),'Vanaf rechts inschuiven. Het losse clipje achteraan voorkomt terugschuiven.',font=font(28),fill=(84,94,94))
 sheet.paste(first,(25,230)); sheet.paste(second,(1025,230)); d=ImageDraw.Draw(sheet)
 d.text((70,196),'Doorsnede: grijze case, blauw voorframe',font=font(29,True),fill=(35,94,87))
 d.text((1070,196),'Uitneembare borgclip met twee veerpootjes',font=font(29,True),fill=(35,94,87))
 d.text((70,855),'Geleiding: 0,25 mm speling per zijde. Print eerst de twee kleine schuifpasstukken. Geometrie is op schaal.',font=font(26),fill=(84,94,94))
 sheet.save(OUT/'Schuifsysteem_detail.png')

def preview(main,bezel,clip):
 body=sb(-SW/2,SW/2,LIFT,SH+LIFT,-15,0)
 active=sb(-43.5,43.5,12.6+LIFT,168.6+LIFT,-15.18,-15.02)
 objects=[(main,(91,107,108)),(bezel,(75,92,94)),(clip,(205,130,52)),(body,(38,40,44)),(active,(31,74,82))]
 first=render_panel(objects,[1.1,-1.8,.85],(1040,1030))
 rear=render_panel(objects,[1.1,1.8,.9],(740,740))
 # Actual horizontal assembly motion. The lock clip is removed for sliding.
 exploded=render_panel([(main,(91,107,108)),(bezel.translate((38,0,0)),(75,92,94)),(body,(38,40,44))],[1,-1.4,.8],(760,570))
 sheet=Image.new('RGB',(1900,1580),(244,244,240)); d=ImageDraw.Draw(sheet)
 d.text((90,50),'CrowPanel 7  /  glad schuifframe',font=font(59,True),fill=(29,42,44))
 d.text((94,138),'Verborgen geleiders  ·  los borgclipje achteraan  ·  geïntegreerde balkjes van 10 mm',font=font(26),fill=(84,94,94))
 sheet.paste(first,(30,210)); sheet.paste(rear,(1100,200))
 sheet.paste(exploded.resize((670,503),Image.Resampling.LANCZOS),(1100,885))
 d=ImageDraw.Draw(sheet)
 d.text((1150,210),'Los borgclipje bovenaan',font=font(28,True),fill=(29,42,44))
 d.text((1155,1360),'Van rechts op de case schuiven',font=font(25,True),fill=(29,42,44))
 d.line((90,1410,1810,1410),fill=(199,208,206),width=2)
 d.text((94,1435),'Voet 126 × 120 mm  |  Gladde voorkant  |  Touchscreen blijft vrij',font=font(26),fill=(29,42,44))
 d.text((94,1482),'18° achterover. Case, schuifframe en borgclip. Ruimte voor de haakse USB-adapter.',font=font(23),fill=(84,94,94))
 d.text((94,1525),'CAD-weergave. Eerst de kleine schuifpasstukken printen. Fysieke proef nog nodig.  v6 · 24 oktober 2026',font=font(21),fill=(105,113,113))
 sheet.save(OUT/'CrowPanel7_schuifframe_ontwerp.png')

if __name__=='__main__': main()
