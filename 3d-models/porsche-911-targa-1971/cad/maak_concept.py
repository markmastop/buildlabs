"""Nieuw 20 cm Targa-vormconcept, handmatig gemodelleerd naar de projectfoto's.
Blender-coördinaten: centimeters. Geen hergebruik van de afgewezen mini.
Run: Blender --background --factory-startup --python maak_concept.py
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
parts=[]
def material(name,color,metal=0,rough=.35):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m
gold=material('Geel-oranje carrosserie',(.95,.43,.015),.12)
silver=material('Zilvergrijze accenten',(.6,.64,.67),.75,.25)
black=material('Zwart rubber',(.015,.02,.025),0,.56)
glass=material('Donkere raaminzetten',(.035,.065,.085),.25,.22)
inside=material('Zwart interieur',(.032,.035,.038),0,.6)
red=material('Achterlicht',(.5,.025,.01),.05)
def finish(o,name,mat):
 o.name=name;o.data.materials.append(mat);parts.append(o)
 if o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
 return o
def active(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def apply(o,m):active(o);bpy.ops.object.modifier_apply(modifier=m.name)
def mesh(name,v,f,mat):
 d=bpy.data.meshes.new(name);d.from_pydata(v,[],f);d.update()
 bm=bmesh.new();bm.from_mesh(d);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(d);bm.free()
 o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);return finish(o,name,mat)
def box(name,pos,size,mat,bevel=.05):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  m=o.modifiers.new('Afgeronde rand','BEVEL');m.width=bevel;m.segments=3;apply(o,m)
 return finish(o,name,mat)
def sphere(name,pos,scale,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=pos);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,mat)
def cylinder(name,pos,r,depth,mat,axis='Y'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=pos,rotation=(math.pi/2,0,0) if axis=='Y' else (0,0,0));return finish(bpy.context.object,name,mat)
def curve(name,points,r,mat):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=3
 s=d.splines.new('POLY');s.points.add(len(points)-1)
 for a,p in zip(s.points,points):a.co=(*p,1)
 o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);return finish(o,name,mat)
def cut(o,tool):
 m=o.modifiers.new('Uitsparing','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=tool;apply(o,m);parts.remove(tool);bpy.data.objects.remove(tool,do_unlink=True)
nodes=[(-9.9,1.7,1.9),(-9.5,2.8,2.02),(-8.7,3.35,2.2),(-7.5,3.65,2.5),(-5.6,3.76,3.0),(-3.1,3.7,3.58),(-1,3.62,3.63),(2,3.64,3.64),(4,3.74,3.65),(5.5,3.85,3.65),(7,3.8,3.4),(8.5,3.5,2.9),(9.5,2.9,2.5),(9.9,2.0,2.35)]
def value(x,col):
 for i in range(len(nodes)-1):
  a,b=nodes[i],nodes[i+1]
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);t=t*t*(3-2*t);return a[col]*(1-t)+b[col]*t
 return nodes[0 if x<nodes[0][0] else -1][col]
v=[];f=[];n=140
for i in range(n):
 x=-9.9+19.8*i/(n-1);w=value(x,1);z=value(x,2)
 bump=1.1*math.exp(-((x+7.6)/2.15)**2)+.38*math.exp(-((x-5.6)/2.1)**2)
 half=[(0,z),(.40*w,z),(.63*w,z+.35*bump),(.81*w,z+.85*bump),(.92*w,z+bump-.15),(.99*w,z+bump-.5),(w,2.3),(.96*w,1.3),(.86*w,1.03),(0,1.03)]
 ring=half+[(-y,zz) for y,zz in reversed(half[1:-1])];N=len(ring)
 v.extend((x,y,zz) for y,zz in ring)
for i in range(n-1):
 for j in range(N):f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
f.extend([tuple(range(N-1,-1,-1)),tuple((n-1)*N+j for j in range(N))])
body=mesh('Carrosserie',v,f,gold);m=body.modifiers.new('Vloeiende carrosserie','SUBSURF');m.levels=2;apply(body,m)
for x in [-5.65,5.25]:
 for side in [-1,1]:cut(body,cylinder('Wielboog',(x,side*3.8,1.5),1.56,1.85,black))
cut(body,box('Cockpit opening',(.75,0,5.5),(5.1,5.55,5.15),black,.4))
box('Cockpit vloer',(.65,0,2.92),(5.3,5.3,.22),inside,.12)

# Gebogen voorruit als dubbel gekromd oppervlak, met een omvattend raamkader.
rows=15;cols=36;v=[];f=[]
for i in range(rows+1):
 t=i/rows;z=3.66+2.37*t;w=3.02-.55*t
 for j in range(cols+1):
  u=-1+2*j/cols;y=w*u;x=-3.12+1.40*t-.28*(1-u*u)
  v.append((x,y,z+.10*(1-u*u)))
for i in range(rows):
 for j in range(cols):
  a=i*(cols+1)+j;f.append((a,a+1,a+cols+2,a+cols+1))
wind=mesh('Gebogen voorruit',v,f,glass)
for ids in [[j for j in range(cols+1)],[rows*(cols+1)+j for j in range(cols+1)],[i*(cols+1) for i in range(rows+1)],[i*(cols+1)+cols for i in range(rows+1)]]:curve('Voorruit kader',[v[k] for k in ids],.065,silver)

# Grote gebogen achterruit; dakzone blijft werkelijk open.
def rear_pos(t,u):
 w=2.83+.29*t;x=3.3+3.85*t+.25*(1-u*u)*t
 edge=abs(u)**2.5
 z=(6.1-2.62*t**1.34)*(1-edge)+(3.60-.12*t)*edge
 return (x,w*u,z)
v=[];f=[]
for i in range(26):
 for j in range(41):v.append(rear_pos(i/25,-1+2*j/40))
for i in range(25):
 for j in range(40):
  a=i*41+j;f.append((a,a+1,a+42,a+41))
mesh('Bolle achterruit',v,f,glass)
curve('Achterruit onderste sierlijst',[rear_pos(1,-1+2*j/60) for j in range(61)],.055,silver)
for side in [-1,1]:curve('Achterruit zijlijst',[rear_pos(i/50,side) for i in range(51)],.055,silver)

# Brede Targaband: gebogen bovenkant en brede zijpanelen; geen smalle poort.
v=[];f=[]
for x in [2.7,3.3]:
 for j in range(61):
  a=math.pi*j/60
  v.append((x,-2.86*math.cos(a),3.59+2.57*(1-abs(math.cos(a))**2.5)))
for j in range(60):f.append((j,j+1,62+j,61+j))
hoop=mesh('Brede Targaband',v,f,silver);m=hoop.modifiers.new('Banddikte','SOLIDIFY');m.thickness=.10;apply(hoop,m)
for side in [-1,1]:
 for x in [2.83,3.00,3.17]:
  curve('Targaband groef',[(x,side*2.86,3.85),(x,side*2.80,4.12),(x,side*2.69,4.45)],.025,black)
for side in [-1,1]:
 box('Zitting',(.5,side*1.27,3.25),(1.85,1.9,.55),inside,.22)
 seat=box('Rugleuning',(1.5,side*1.27,4.12),(.48,1.95,1.94),inside,.22);seat.rotation_euler[1]=math.radians(-10)
box('Dashboard',(-2.1,0,3.85),(.65,5.4,.6),inside,.17)
bpy.ops.mesh.primitive_torus_add(major_radius=.52,minor_radius=.055,major_segments=48,minor_segments=12,location=(-1.43,-1.2,4.15),rotation=(0,math.pi/2+.35,0));finish(bpy.context.object,'Stuur',inside)
curve('Stuurkolom',[(-1.43,-1.2,4.15),(-2.1,-1.2,3.75)],.07,inside)

# Vier normale wielmaten met vijf radiale velgbladen.
for x in [-5.65,5.25]:
 for side in [-1,1]:
  tyre=cylinder('Band',(x,side*3.38,1.5),1.4,.88,black)
  m=tyre.modifiers.new('Ronde bandwang','BEVEL');m.width=.14;m.segments=4;apply(tyre,m)
  cylinder('Donkere velgbasis',(x,side*3.84,1.5),1.08,.08,inside)
  bpy.ops.mesh.primitive_torus_add(major_radius=1.07,minor_radius=.055,major_segments=64,minor_segments=10,location=(x,side*3.9,1.5),rotation=(math.pi/2,0,0));finish(bpy.context.object,'Velgrand',silver)
  for k in range(5):
   a=2*math.pi*k/5;petal=box('Vijfbladig wielhart',(x+.5*math.sin(a),side*3.91,1.5+.5*math.cos(a)),(.29,.10,.92),silver,.12);petal.rotation_euler[1]=a
  cylinder('Wielnaaf',(x,side*3.98,1.5),.3,.10,silver)

# Lampen volgen het schuine voorvlak van de spatborden.
for side in [-1,1]:
 lamp=sphere('Koplamp sierring',(-8.38,side*2.94,3.03),(.71,.71,.10),silver);lamp.rotation_euler[1]=-.92
 lamp=sphere('Koplampglas',(-8.45,side*2.94,3.08),(.60,.60,.10),silver);lamp.rotation_euler[1]=-.92
 box('Voorste lichtunit',(-9.46,side*2.53,1.95),(.20,1.15,.27),silver,.08)
 box('Achterlicht',(9.53,side*2.10,2.25),(.15,1.20,.27),red,.08)
 # Deurlijn ligt aan de flank; alle merkdetails blijven neutraal.
 curve('Deurnaad',[(-2.50,side*3.66,3.48),(-2.7,side*3.66,1.68),(-2.4,side*3.65,1.46),(2.65,side*3.68,1.46),(3.0,side*3.70,1.7),(3.0,side*3.70,3.48)],.018,inside)
 box('Deurgreep',(1.55,side*3.70,3.32),(.65,.09,.13),silver,.05)
 curve('Dorpellijst',[(-3.9,side*3.57,1.32),(3.7,side*3.59,1.32)],.045,silver)
for front in [True,False]:
 x=-10.02 if front else 10.02
 points=[(x+.46*(abs(u)**2)*(1 if front else -1),3.0*u,1.60 if front else 1.68) for u in [-1+2*j/40 for j in range(41)]]
 curve('Bumper rubber',points,.15,black)
 curve('Bumper sierlijst',[(a,b,c+.10) for a,b,c in points],.065,silver)
for x in [7.2,7.38,7.56,7.74,7.92,8.10,8.28]:
 z=value(x,2)+.02;curve('Motorrooster',[(x,-1.55,z),(x,1.55,z)],.035,inside)
mirror=sphere('Linker spiegel',(-2.65,-3.82,4.0),(.27,.13,.23),silver)
curve('Spiegelvoet',[(-2.65,-3.55,3.65),(-2.65,-3.82,3.94)],.055,silver)

# Bewerkbare bron en kijkmesh zijn exact dezelfde verzameling onderdelen.
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.01
active(body)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
meshparts=[o for o in parts if o.type=='MESH']
bounds=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
report={'status':'eerste vormconcept; geen printklaar model','eenheid':'centimeter','maten_cm':[round(max(v[i] for v in bounds)-min(v[i] for v in bounds),3) for i in range(3)],'objecten':len(parts),'meshes':len(meshparts),'bron':'Nieuwe handmatige parametrische opbouw op basis van eigen foto’s en 20cm-beeldvoorstel; geen scan of exacte schaalreconstructie.','printcontrole':False}
(OUT/'modelgegevens.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
bpy.ops.export_scene.gltf(filepath=str(OUT/'911-targa-concept-v1.glb'),export_format='GLB',use_selection=True,export_yup=True)

floor=box('Studiovloer',(0,0,-.10),(200,200,.16),material('Studio',(.80,.80,.77)),.02)
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.world.color=(.3,.3,.3)
scene.render.resolution_x=1440;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for pos,power,size in [((-15,-25,32),19000,20),((10,25,25),13000,18),((25,5,28),18000,16)]:
 d=bpy.data.lights.new('Studio','AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new('Studio',d);bpy.context.collection.objects.link(o);o.location=pos;aim(o,(0,0,2))
d=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',d);bpy.context.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.ortho_scale=25
cam.location=(-28,-32,20);aim(cam,(0,0,2.7))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'911-targa-concept-v1.blend'))
scene.render.filepath=str(OUT/'voorzijde.png');bpy.ops.render.render(write_still=True)
cam.location=(28,-32,18);aim(cam,(0,0,2.7));scene.render.filepath=str(OUT/'achterzijde.png');bpy.ops.render.render(write_still=True)
print(json.dumps(report))
