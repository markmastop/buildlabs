"""Details van vormstudie v3 als echte CAD-/printgeometrie. Eenheden mm.
Geen uitsluitend grafische decoratie: iedere toevoeging krijgt een STEP/STL/3MF.
"""
import math
import cadquery as cq
import numpy as np


def beam(a,b,w=1.2):
 a=cq.Vector(*a);d=cq.Vector(*b)-a
 # Planar begrensde balkjes vermijden minieme snijranden van veel ronde buisjes.
 xd=(1,0,0) if abs(d.normalized().x)<.95 else (0,1,0)
 return cq.Workplane(cq.Plane(origin=a,normal=d,xDir=xd)).rect(w,w).extrude(d.Length)


def helicopter_windows(body,sections):
 """Losse gebogen cockpitruiten met rand- en bodemspeling in de gele helften."""
 def interp(x):
  for a,b in zip(sections,sections[1:]):
   if x<=b[0]:
    t=(x-a[0])/(b[0]-a[0]);return [a[k]+t*(b[k]-a[k]) for k in range(1,4)]
  return sections[-1][1:]
 def patch(x0,x1,a0,a1,outer,inner):
  xs=sorted(set([x0,x1]+[a[0] for a in sections if x0<a[0]<x1]))
  wires=[]
  for x in xs:
   z,rz,ry=interp(x);angles=np.linspace(a0,a1,15)
   pts=[((ry+outer)*math.sin(a),z+(rz+outer)*math.cos(a)) for a in angles]
   pts += [((ry+inner)*math.sin(a),z+(rz+inner)*math.cos(a)) for a in angles[::-1]]
   wires.append(cq.Workplane('YZ',origin=(x,0,0)).polyline(pts).close().wire().val())
  return cq.Workplane(obj=cq.Solid.makeLoft(wires,ruled=True))
 caps=[]
 for sd in [-1,1]:
  for k,(x0,x1,a0,a1) in enumerate([(-30.5,-18.5,.14,1.35),(-17,-5.5,.56,1.5),(-3.8,6.5,.62,1.5)]):
   cut=patch(x0,x1,sd*a0,sd*a1,.25,-.95)
   body=body.cut(cut)
   cap=patch(x0+.12,x1-.12,sd*(a0+.015),sd*(a1-.015),.15,-.80)
   caps.append((f'64_heli_ruit_{"BB" if sd>0 else "SB"}_{k+1}',cap))
 return body,caps


def masts(api):
 add,box,join,rod,wire,offset=[api[k] for k in ['add','box','join','rod','wire','offset']]
 white,black=api['WHITE'],api['BLACK']
 # Vier losse, taps toelopende vakwerkvlakken: een echte ruimtelijke mast.
 height=math.hypot(99,5.7)
 pl=cq.Plane(origin=(333,-7.5,255),xDir=(1,0,0),normal=(0,-99,5.7))
 panel=cq.Workplane(pl).polyline([(-7.5,0),(7.5,0),(1.8,height),(-1.8,height)]).close().extrude(1.2)
 for k in range(7):
  v0=height*k/7;v1=height*(k+1)/7;b0=7.5-5.7*k/7;b1=7.5-5.7*(k+1)/7
  # Twee driehoekige vensters per vak met een doorlopende diagonaal ertussen.
  tris=[[(-b0,v0),(b0,v0),(b1,v1)],[(-b0,v0),(b1,v1),(-b1,v1)]]
  if k%2:tris=[[(-b0,v0),(b0,v0),(-b1,v1)],[(b0,v0),(b1,v1),(-b1,v1)]]
  for pts in tris:
   try:
    iw=offset(wire(pts),.8)
    xy=[(v.X,v.Y) for v in iw.Vertices()]
    panel=panel.cut(cq.Workplane(pl).polyline(xy).close().extrude(2))
   except (ValueError,IndexError):pass  # Het smalste topvak kan geen tweede gat bevatten.
 for z in [292,315,336]:
  v=(z-255)*height/99;bw=7.5-5.7*(z-255)/99
  panel=panel.union(cq.Workplane(pl).center(0,v).rect(2*bw,1.6).extrude(1.2))
 for i,label in enumerate(['voor','SB','achter','BB']):
  face=panel.rotate((333,0,255),(333,0,256),i*90)
  angle=math.degrees(math.atan2(-99,5.7))
  axis=(1,0,0) if i%2==0 else (0,1,0)
  if i in [1,2]:angle=-angle
  add('32_vakwerk_'+label,face,black,rotate=(axis,angle),note='Vier taps toelopende vlakken tot een ruimtelijke mast verlijmen; breedte onder 15, boven 3,6 mm.')
 top=join([box(6,6,1.2,333,0,353.4),rod((333,0,354),(333,0,374),.8)])
 add('32_masttop',top,black,rotate=((1,0,0),90))
 for i,(z,length) in enumerate([(292,54),(315,48),(336,38)]):
  add('32_ra_'+str(i+1),box(2,length,1.6,333,0,z-.8),black,note='Lijmen op de dwarsbanden van de vier vakwerkvlakken.')
 # Radarmast, schuine mantel, twee werkplatforms en twee echte scanners.
 add('33_radarmast',rod((589,0,226),(589,0,338),4.2).union(rod((589,0,337),(589,0,362),1)),white,rotate=((1,0,0),90))
 mantle=api['xz_panel']([(562,193),(585,193),(585,274),(581,274)],7.5,15)
 add('33_mastmantel',mantle,white,rotate=((1,0,0),90))
 for i,(x,z,w,d,rx,length) in enumerate([(599,266,32,66,603,60),(595,296,24,46,598,42)]):
  floor=box(w,d,1.5,x,0,z).cut(cq.Workplane('XY').center(589,0).circle(4.45).extrude(5).translate((0,0,z-1)))
  add('33_radarplatform_'+str(i+1),floor,white)
  add('33_radarvoet_'+str(i+1),box(7,7,5.5,rx,0,z+1.5),black)
  scanner=join([box(5,5,1.8,rx,0,z+7),box(2.8,length,4.2,rx+.5,0,z+8.5)])
  add('33_radarscanner_'+str(i+1),scanner,'#65747c')
 cross=join([beam((589,-36,320),(589,36,320),1.6),box(5,5,3,589,0,318.5)])
 add('33_mastdwarsarm',cross,white)
 add('35_brugvoormast',join([rod((690,0,226),(690,0,292),2),beam((690,-22,272),(690,22,272),1.6),box(12,20,1.2,690,0,256)]),white,rotate=((1,0,0),90))


def davits_cranes(api):
 add,box,join,rod=[api[k] for k in ['add','box','join','rod']]
 for sd,label in [(1,'BB'),(-1,'SB')]:
  joints=[(-6,sd*76.5,139),(-6,sd*80,160),(0,sd*95,172),(5,sd*91,216),(3.5,sd*86,222)]
  bars=[]
  for dx in [-1.7,1.7]:
   for a,b in zip(joints,joints[1:]):bars.append(beam((a[0]+dx,a[1],a[2]),(b[0]+dx,b[1],b[2]),1.9))
  for p in joints:bars.append(beam((p[0]-2.65,p[1],p[2]),(p[0]+2.65,p[1],p[2]),1.4))
  add('41_davit_'+label,join(bars),api['ORANGE'],qty=2,placements=[(313,0,0),(379,0,0)],rotate=((0,1,0),90),note='Dubbele geknikte armen met dwarsverbindingen, volgens vormstudie v3.')
  cyl=rod((-4,sd*76,156),(2,sd*89,183),1.05)
  add('41_hydrauliek_'+label,cyl,'#737e83',qty=2,placements=[(313,0,0),(379,0,0)],rotate=((0,1,0),90))
  # De kraanarm volgt de lagere, lange knikarm uit het visuele model.
  x,y=552,sd*66;z=194.1
  crane=join([rod((x,y,z),(x,y,z+16),5),box(10,9,7,x,y,z+15.5),beam((x,y,z+21),(x-42,y+sd*6,z+28),4),beam((x-42,y+sd*6,z+28),(x-64,y+sd*9,z+24.5),3)])
  add('42_dekkraan_'+label,crane,api['ORANGE'],rotate=((1,0,0),90))
  add('42_kraancilinder_'+label,beam((x+2,y,z+15),(x-16,y+sd*2.5,z+24),2),api['BLACK'],rotate=((1,0,0),90))


def enrich(a):
 add,box,join,rod,poly,plan,clip,hollow=[a[k] for k in ['add','box','join','rod','poly','plan','clip','hollow_plan']]
 white,black,green,orange,navy=[a[k] for k in ['WHITE','BLACK','GREEN','ORANGE','NAVY']]
 # Donkere inzetruiten liggen achter de echte raamgaten, zodat de openingen
 # in de assemblage niet groen van het dek lijken. Ook als foliesjabloon te gebruiken.
 off,prism,wire=[a[k] for k in ['offset','prism','wire']]
 def glazing(pts,z,h):
  w=wire(pts,z);return prism(off(w,1.7),h).cut(prism(off(w,2.5),h+2).translate((0,0,-1)))
 glass=glazing(plan(175,714,82,4,30),148.2,6.5)
 for i,(x0,x1) in enumerate([(175,355),(355,535),(535,714)]):
  for sd,label in [(1,'BB'),(-1,'SB')]:
   side=clip(glass,x0,x1).intersect(box(1000,120,100,450,sd*60,100))
   add(f'19_ruitstrook_laag_{i+1}_{label}',side,'#182d3a',note='Inzet achter accommodatievensters; transparant printen of als snijmal voor folie gebruiken.')
 add('19_ruitstrook_binnenhuis',glazing(plan(420,608,46.5,3.5,3.5),175.2,11.2),'#182d3a')
 add('19_ruitstrook_voorhuis',glazing(plan(605,698,67,4,22),176.8,7.2),'#182d3a')
 outline=wire([(585,-56),(589,-60),(641,-60),(641,-75),(646,-80),(691,-80),(696,-75),(696,75),(691,80),(646,80),(641,75),(641,60),(589,60),(585,56)],206.8)
 bridgeglass=prism(off(outline,1.7),12).cut(prism(off(outline,2.5),14).translate((0,0,-1)))
 # Het tussenschot van de bestaande brug vraagt twee inzetstukken.
 # De sneden laten circa 0,2 mm vrij van de witte retouren bij X=641.
 for y in [-57.9,57.9]:bridgeglass=bridgeglass.cut(box(3.6,1.2,14,641,y,205.8))
 for i,part in enumerate(bridgeglass.solids().vals()):
  add('19_brugbeglazing_'+str(i+1),part,'#182d3a',note='Twee passende brug-inzetstukken; circa 0,2 mm vrij van het tussenschot. Ook als foliesjabloon te gebruiken.')
 # De juiste relingen staan daadwerkelijk in de assemblage, geen losse voorraadstroken.
 rails=[]
 def railing(label,pts,z,h=9.5,step=11):
  count=0
  for p,q in zip(pts,pts[1:]):
   d=np.array(q)-p;length=float(np.linalg.norm(d))
   if length<.1:continue
   n=max(1,math.ceil(length/220))
   for j in range(n):
    u=np.array(p)+d*j/n;v=np.array(p)+d*(j+1)/n;run=float(np.linalg.norm(v-u));count+=1
    bars=[beam((*u,z+t*h),(*v,z+t*h),1.2) for t in [.33,.66,1]]
    for t in np.linspace(0,1,max(2,math.ceil(run/step)+1)):
     xy=u+(v-u)*t;bars.append(beam((*xy,z),(*xy,z+h),1.4))
    if h<6:
     # Bij korte radarhekken moet iedere rail op dezelfde vlakke achterkant
     # beginnen. Het verschil van 0,1 mm tussen buisjes en palen gaf anders
     # onbereikbare steunregio's op de eerste laag.
     direction=(v-u)/run;normal=(direction[1],-direction[0],0)
     origin=(u[0]-.7*normal[0],u[1]-.7*normal[1],z)
     pl=cq.Plane(origin=origin,xDir=(*direction,0),normal=normal)
     bars=[cq.Workplane(pl).center(run/2,t*h).rect(run+1.4,1.2).extrude(1.4) for t in [.33,.66,1]]
     for t in np.linspace(0,1,max(2,math.ceil(run/step)+1)):
      bars.append(cq.Workplane(pl).center(run*t,h/2).rect(1.4,h).extrude(1.4))
    # Leg het paneel vlak: draaien rond zijn lengterichting.
    axis=tuple((v-u).tolist()+[0])
    add(f'70_reling_{label}_{count}',join(bars),'#d0d6d7',rotate=(axis,90),note='Op maat gemaakt relingpaneel; plaats zie CAD-assemblage. Rails 1,2 / staanders 1,4 mm.')
  rails.append(label)
 for sd,label in [(1,'BB'),(-1,'SB')]:
  railing('laag_achter_'+label,[(178,sd*80),(310,sd*80),(442,sd*80)],166.9)
  railing('laag_voor_'+label,[(450,sd*80),(570,sd*80),(686,sd*80)],166.9)
  railing('galerijdak_'+label,[(415,sd*69),(527,sd*69),(639,sd*69)],194.1)
 compass=[(585,-60.5),(641,-60.5),(641,-80.5),(692,-80.5),(697,-75.5),(697,75.5),(692,80.5),(641,80.5),(641,60.5),(585,60.5),(585,-60.5)]
 railing('kompasdek',compass,226,9)
 hangar=[(174,-80.5),(299,-80.5),(299,-62.5),(368.5,-62.5),(368.5,62.5),(299,62.5),(299,80.5),(174,80.5),(174,-80.5)]
 railing('hangardak',hangar,207,9)
 for i,(x,z,w,d) in enumerate([(599,267.5,30,66),(595,297.5,22,46)]):
  railing('radar'+str(i+1),[(x-w/2,-d/2),(x+w/2,-d/2),(x+w/2,d/2),(x-w/2,d/2),(x-w/2,-d/2)],z,5.5,7)
 # Trappen met treden, twee doorlopende bomen en echte leuningen.
 def stairs(label,x,width,z0,z1,y0,y1):
  n=max(4,round(abs(z1-z0)/4.2));pieces=[]
  for dx in [-width/2,width/2]:
   pieces.append(beam((x+dx,y0,z0),(x+dx,y1,z1),1.4))
   pieces.append(beam((x+dx,y0,z0+9),(x+dx,y1,z1+9),1.2))
   for t in [0,.33,.66,1]:
    y=y0+(y1-y0)*t;z=z0+(z1-z0)*t;pieces.append(beam((x+dx,y,z),(x+dx,y,z+9),1.2))
  for t in np.linspace(0,1,n+1):
   y=y0+(y1-y0)*t;z=z0+(z1-z0)*t;pieces.append(box(width+1.2,3.8,1.2,x,y,z-.6))
  add('71_trap_'+label,join(pieces),'#aab5b9',rotate=((0,1,0),90),note='Treden en leuningen in één deel. Boomsteunen controleren.')
 for sd,label in [(1,'BB'),(-1,'SB')]:
  stairs('galerij_'+label,407.5,9,166.9,193,sd*39,sd*63)
  stairs('hangar_'+label,374.5,9,166.9,205,sd*14,sd*42)
  stairs('brug_'+label,578.5,9,194.1,226,sd*10,sd*45)
  stairs('helidek_'+label,163.5,9,140,167.5,sd*20,sd*50)
 # Helideknetten: vijf losse roosterpanelen met naar buiten aflopend vlak.
 hp=plan(0,175,89,18,10)
 for i,p in enumerate(hp):
  if i in [1,2,3]:continue
  q=hp[(i+1)%len(hp)];d=np.array(q)-p;length=float(np.linalg.norm(d));out=np.array([d[1],-d[0]])/length
  pieces=[]
  def pt(t,s):
   xy=np.array(p)+d*t+out*s;return (*xy,167.0-.24*s)
  for t in np.linspace(0,1,max(2,math.ceil(length/8)+1)):pieces.append(beam(pt(t,0),pt(t,10),1.2))
  for s in [0,3.3,6.6,10]:pieces.append(beam(pt(0,s),pt(1,s),1.2))
  add('72_helideknet_'+str(i+1),join(pieces),'#c8d0d3',rotate=((float(d[0]),float(d[1]),0),-math.degrees(math.atan(.24))),note='Roosterframe 1,2 mm, vlak voorgedraaid. Aan rand helidek verlijmen.')
 # Dichte witte verschansing rond de achterste promenade.
 pp=plan(2,242,87,16.5,4)
 wall=clip(hollow(pp,139,11.2,1.4),0,175)
 add('73_achterverschansing',wall,white)
 # Blauwe verschansing met opening voor de valreep.
 bars=[];pts=[(240,-85.5),(2,-85.5),(0,-70),(0,70),(2,85.5),(130,85.5)]
 for p,q in zip(pts,pts[1:]):
  d=np.array(q)-p;mid=(np.array(p)+q)/2
  b=box(float(np.linalg.norm(d))+1.5,1.6,12,0,0,107).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(d[1],d[0]))).translate((*mid,0));bars.append(b)
 add('73_werkdekverschansing',join(bars),navy)
 add('73_werkdekverschansing_BB_voor',box(94,1.6,12,193,85.5,107),navy)
 # Achterste dwarstank met zadels.
 tank=rod((14,-72,147.5),(14,-8,147.5),7.5)
 tank=join([tank,box(9,3,2,14,-13,139),box(9,3,2,14,-67,139)])
 add('74_achtertank',tank,'#e0e0d9',rotate=((1,0,0),90))
 # Hangarspanten, kabinetten, werkbok en blade-racks.
 for i,x in enumerate([195,223,251,279]):
  frame=join([box(1.6,1.3,34.5,x,-77,168.1),box(1.6,1.3,34.5,x,77,168.1),box(1.6,155,2.2,x,0,202.3)])
  add('75_hangarspant_'+str(i+1),frame,'#d2d7d9',rotate=((0,1,0),90))
 cabinet=box(13,14,17).cut(box(11,.6,14,0,-6.9,1.5)).union(box(.8,.7,14,0,-7,1.5))
 add('75_hangarkast',cabinet,'#718079',qty=2,placements=[(278,-57,168.1),(278,57,168.1)])
 table=join([box(8,10,13.5,227,0,168.1),box(11,13,1.2,227,0,181.6)])
 add('75_werkbok',table,white)
 rack=box(58,8,6).cut(box(55.6,5.6,8,0,0,1.6))
 add('75_rotorbladenrek',rack,black,qty=2,placements=[(224,-69,168.1),(224,69,168.1)])
 add('75_dakkast',box(14,16,10,196,0,207),white)
 # Sloepdetails: donkere afzonderlijke raamstroken, hutdakjes en stootranden.
 for sd,label in [(1,'BB'),(-1,'SB')]:
  # Glazing strip follows the shoulder slope of the actual p1 lifeboat body.
  z0,z1=17.5,20.5;y0=14.2-(z0-12)*5.9/14;y1=14.2-(z1-12)*5.9/14
  pl=cq.Plane(origin=(0,sd*y0,z0),xDir=(-sd,0,0),normal=(0,sd*3,y0-y1))
  strip=cq.Workplane(pl).rect(46,.7).extrude(.7)  # hidden connector along row
  for x in np.linspace(-22,22,9):strip=strip.union(cq.Workplane(pl).center(float(x),1.4).rect(3.5,2.8).extrude(.8))
  add('76_sloep_raamstrook_'+label,strip,black,qty=2,placements=[(346,-89,176.5),(346,89,176.5)])
 hatch=join([box(8,7,4.2,-26.8,0,26),box(1.2,7,1,-22.8,0,29.2)])
 add('76_sloep_dakluik',hatch,white,qty=2,placements=[(346,-89,176.5),(346,89,176.5)])
 # Lichtkap met witte roeden op schuine glasvlakken.
 pieces=[]
 for x in [492.8,511.3,529.8,548.3]:
  pieces.extend([beam((x,-29,198),(x,0,204.9),1.2),beam((x,0,204.9),(x,29,198),1.2)])
 pieces.extend([beam((492.8,0,204.9),(548.3,0,204.9),1.2),beam((492.8,-29,198),(548.3,-29,198),1.2),beam((492.8,29,198),(548.3,29,198),1.2)])
 add('77_lichtkap_roeden',join(pieces),white)
 # Radardomes en antennevoetjes op het kompasdek.
 # Y = bakboord positief: de grote dome staat in de vormstudie aan bakboord (was gespiegeld).
 for i,(x,y,r) in enumerate([(656,52,10.5),(656,-52,8.5),(612,34,5.5),(612,-34,5.5)]):
  dome=cq.Workplane('XY').sphere(r).translate((x,y,235+r*.7)).union(rod((x,y,226),(x,y,235),3.5))
  add('78_satcom_'+str(i+1),dome,white)
 add('78_brugdomes',join([box(12,20,1.2,690,0,256),cq.Workplane('XY').sphere(4.5).translate((690,-6,261.5)),cq.Workplane('XY').sphere(4.5).translate((690,6,261.5))]),white)
 for i,(x,y) in enumerate([(668,-18),(668,18),(600,-45)]):
  gps=join([rod((x,y,226),(x,y,234),1),rod((x,y,233),(x,y,237),2.5)])
  add('78_GPS_'+str(i+1),gps,white)
 for i,(x,y,h) in enumerate([(590,55,55),(592,-55,46),(650,68,34),(650,-68,34),(616,15,30)]):
  add('78_antenne_'+str(i+1),rod((x,y,226),(x,y,226+h),.65),'#c4cdd1',rotate=((1,0,0),90))
 lamp=join([box(5,5,2,0,0,0),rod((0,0,1),(0,0,5),1.5),rod((-3.5,0,6),(3.5,0,6),3.6)])
 add('78_zoeklicht',lamp,'#d2d9dc',qty=2,placements=[(692,-66,226),(692,66,226)])
 # Schoorsteen: donkere achterwand en drie schuine uitlaten.
 add('79_schoorsteen_achtervlak',box(1.2,47,40,263.6,0,210),black)
 cone=cq.Workplane(obj=cq.Solid.makeCone(3.8,3.4,13)).rotate((0,0,0),(0,1,0),-math.degrees(.5))
 add('79_uitlaat',cone,'#c6ced0',qty=3,placements=[(317.12,0,254.3),(302.12,0,254.3),(287.12,0,254.3)])
 # Zodiacs: open kuip, pontons, spiegel en buitenboordmotor in één print.
 def zodiac():
  pts=[(-19.5,-6.2),(.6,-6.2),(16,-4.5),(21,0),(16,4.5),(.6,6.2),(-19.5,6.2)]
  pieces=[box(36,10.5,1.2,-1,0,0),box(1.6,10.5,4.5,-19.2,0,0),box(4,3.5,4.2,4,0,1.2),box(4.5,3.6,5,-21.8,0,4),box(1.6,1.6,7.5,-22,0,-2)]
  for p,q in zip(pts,pts[1:]):
   pieces.append(rod((*p,3),(*q,3),2.7))
  return join(pieces)
 zod=zodiac()
 add('80_zodiac',zod,'#3d454a',qty=6,placements=[(459,y,168.2+k*6.8) for y in [-62.5,62.5] for k in range(3)])
 add('80_reddingsrib',zod,orange,qty=2,placements=[(255,-89.5,168.2),(255,89.5,168.2)])
 for sd,label in [(1,'BB'),(-1,'SB')]:
  add('80_RIB_platform_'+label,box(52,20.5,1.8,255,sd*89.5,165.1),white)
  dv=join([beam((285,sd*86.5,166.9),(285,sd*86.5,200.9),3.6),beam((285,sd*86.5,200.9),(255,sd*91,204.9),3)])
  add('80_RIB_davit_'+label,dv,orange,rotate=((1,0,0),90))
 # Reddingsvlotkokers met donkere spanbanden.
 can=rod((0,-6.5,0),(0,6.5,0),4.8).union(box(9,12,2,0,0,-5.8))
 add('81_reddingsvlot',can,white,qty=4,placements=[(x,y,173.4) for x in [650,670] for y in [-74,74]])
 rings=cq.Workplane(obj=cq.Solid.makeTorus(4.2,1.1)).rotate((0,0,0),(1,0,0),90)
 add('81_reddingsboei',rings,orange,qty=6,placements=[(x,y,172.9) for x in [270,460,570] for y in [-82,82]],rotate=((1,0,0),90))
 # Vlaggenstok en windsok als losse, stevige modelonderdelen.
 add('82_windsokmast',rod((214,0,207),(214,0,247),.8),'#bac4c9',rotate=((1,0,0),90))
 sock=cq.Workplane(obj=cq.Solid.makeCone(1.2,3,16,cq.Vector(198,0,246),cq.Vector(1,0,0)))
 add('82_windsok',sock,'#e9562d')
 add('82_vlaggenstok',rod((13,-65,167.5),(13,-65,202.5),.8),'#bac4c9',rotate=((1,0,0),90))
 for i,(color,z) in enumerate([('#21468b',188.5-8),('#eeeeea',188.5-8+16/3),('#ae1c28',188.5-8+32/3)]):
  add('82_vlagstrook_'+str(i+1),box(24,.8,16/3,1,-65,z),color,rotate=((1,0,0),90))
 # Winches, bitts and mushroom vents follow the original foredeck stations.
 winch=join([box(18,16,4),box(6,10,4,0,0,4),rod((0,-3.5,8.5),(0,3.5,8.5),4.2),box(7,4.5,5.5,-9,0,4)])
 add('83_ankerlier',winch,'#687b85',qty=2,placements=[(820,-20,139),(820,20,139)])
 gypsy=rod((0,-1.1,0),(0,1.1,0),5.5)
 add('83_kettingschijf',gypsy,black,qty=2,placements=[(820,-24.75,147.5),(820,24.75,147.5)],rotate=((1,0,0),90))
 def hw(x,z):
  hw,aa,bb=a['station'](z);t=(x-aa)/(bb-aa)
  return hw*math.sqrt(max(0,1-(max(0,t-.58)/.42)**2))
 bitts=join([box(14,6,1.2),rod((-4,0,1),(-4,0,7.2),2.2),rod((4,0,1),(4,0,7.2),2.2)])
 add('83_bolder',bitts,black,qty=4,placements=[(x,sd*(hw(x,139)-inset),139) for x,inset in [(730,11),(864,8)] for sd in [-1,1]])
 vent=join([rod((0,0,0),(0,0,8),2),rod((0,0,7.5),(0,0,10),4.2)])
 add('83_luchtkoker',vent,white,qty=4,placements=[(x,sd*y,139) for x,y in [(760,42),(725,24)] for sd in [-1,1]])
 add('83_bakluik',box(30,32,6,755,0,139),green)
 # Patrijspoorten als gesloten opzetdetails: de natte romp blijft onaangetast.
 disk=rod((0,0,0),(0,.8,0),1.7)
 poses=[]
 for z,xs in [(123,[270,305,340,375,410,445,480,515,550,585,620,655,690,725,760,790]),(72,[280,320,360,400,440,480,520,560,600])]:
  for x in xs:
   poses.append((x,hw(x,z)+.15,z));poses.append((x,-hw(x,z)-.95,z))
 add('84_patrijspoort',disk,'#182d3a',qty=len(poses),placements=poses,rotate=((1,0,0),90),note='Optionele gesloten opzetplaatjes; schilderen kan ook. Geen gaten onder de waterlijn maken.')
 # Ankers, valreep en horizontaal gestuwde trap.
 for sd,label in [(1,'BB'),(-1,'SB')]:
  anchor=join([box(5,2,15,818,sd*hw(818,76),62),box(12,3,3.5,818,sd*hw(818,76),60)])
  add('85_anker_'+label,anchor,black,rotate=((1,0,0),90))
 pieces=[]
 start=np.array([138,89,109.5]);end=np.array([199,89,65.5])
 for dy in [-4.2,4.2]:
  p=start+np.array([0,dy,0]);q=end+np.array([0,dy,0]);pieces.extend([beam(p,q,1.4),beam(p+[0,0,8.5],q+[0,0,8.5],1.2)])
  for t in np.linspace(0,1,7):
   v=p+(q-p)*t;pieces.append(beam(v,v+[0,0,8.5],1.2))
 for t in np.linspace(0,1,17):
  p=start+(end-start)*t;pieces.append(box(3.8,9.6,1.2,p[0],p[1],p[2]-.6))
 add('85_valreep_BB',join(pieces),'#a2afb4',rotate=((1,0,0),90))
 stored=join([box(106,1.2,1.2,110,-88,110.5),box(106,1.2,1.2,110,-88,115.5)]+[box(1.2,1.2,5,x,-88,111) for x in np.linspace(58,162,22)])
 add('85_valreep_SB_gestuwd',stored,'#a2afb4',rotate=((1,0,0),90))
 # Naamplaten op het kompasdek: gegraveerde letters behouden het detail
 # ook zonder decals; de groeven kunnen donker worden ingewassen.
 nameplate=box(40,7.5,1,0,0,0)
 text=cq.Workplane('XY').text('ORTELIUS',4.4,.8,font='Arial',kind='bold',combine=False).translate((0,0,.4))
 nameplate=nameplate.cut(text).rotate((0,0,0),(1,0,0),90)
 nameplate=join([nameplate,box(2,2,2,-14,-.5,-4.75),box(2,2,2,14,-.5,-4.75)])
 for sd,label in [(-1,'SB'),(1,'BB')]:
  plaque=nameplate if sd<0 else nameplate.rotate((0,0,0),(0,0,1),180)
  add('86_naamplaat_'+label,plaque.translate((608,sd*60.7,230.5)),white,rotate=((1,0,0),90*sd),note='Gegraveerde scheepsnaam; letters donker inwassen. Twee steunpootjes op het kompasdek.')
 # Bronverantwoording voor de detailcontrole naast de exportlijst.
 a['detail_report']={'source':'../index.html vormstudie v3, posities ×10 en assen X/-Z/Y','rail_groups':rails,'restored':['Relingen op de juiste dekken','Acht trappen met leuningen','Vijf helideknetten','Ruimtelijke vakwerkmast','Radarplatforms en scanners','Dome-antennes en zoeklichten','Dubbele sloepdavits met hydrauliek','Ramen, lichtkaproeden, uitlaten','Hangarspanten, kasten en rotorrekken','Zodiacs en RIB-davits','Tank, boeien, vlag en windsok','Ankerlieren, bolders, luchtkokers','Patrijspoorten, ankers en valreep']}
