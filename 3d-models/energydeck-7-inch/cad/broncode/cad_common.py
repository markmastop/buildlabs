from pathlib import Path
import math, struct
from collections import Counter
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def mesh_report(path,shape):
    # Validate the actual binary STL, with welded shared coordinates.
    data=Path(path).read_bytes()
    count=struct.unpack_from('<I',data,80)[0]
    edges=Counter(); degenerate=0; volume=0.0
    for i in range(count):
        vals=struct.unpack_from('<12fH',data,84+50*i)
        pts=[tuple(round(v,5) for v in vals[j:j+3]) for j in [3,6,9]]
        aa,bb,cc=map(np.array,pts)
        if np.linalg.norm(np.cross(bb-aa,cc-aa))<1e-7: degenerate+=1
        volume+=float(np.dot(aa,np.cross(bb,cc))/6)
        for j in range(3): edges[tuple(sorted((pts[j],pts[(j+1)%3])))]+=1
    b=shape.val().BoundingBox()
    r={'file':Path(path).name,'valid_brep':shape.val().isValid(),
       'solid_count':len(shape.val().Solids()),'triangles':count,
       'boundary_or_nonmanifold_edges':sum(v!=2 for v in edges.values()),
       'degenerate_triangles':degenerate,'signed_mesh_volume_mm3':round(volume,2),
       'cad_volume_mm3':round(shape.val().Volume(),2),
       'envelope_mm':[round(b.xlen,2),round(b.ylen,2),round(b.zlen,2)]}
    assert r['valid_brep'] and r['solid_count']==1,r
    assert r['boundary_or_nonmanifold_edges']==0 and degenerate==0 and volume>0,r
    assert max(r['envelope_mm'])<256,r
    assert abs(volume-shape.val().Volume())/shape.val().Volume()<.002,r
    return r

def font(size,bold=False):
    choices=[Path(__file__).parent/'Manrope.ttf',
             Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf')]
    for p in choices:
        if p.exists():
            f=ImageFont.truetype(str(p),size)
            if p.name=='Manrope.ttf': f.set_variation_by_axes([700 if bold else 450])
            return f
    return ImageFont.load_default(size)

def shape_triangles(shape,color):
    vs,fs=shape.val().tessellate(0.15,0.18)
    vv=np.array([v.toTuple() for v in vs],dtype=float)
    return [(vv[list(t)],color) for t in fs]

def render_panel(objects, camera, size=(1000,1000),bounds=None):
    """Orthographic shaded CAD render, using triangles from the exported solids."""
    tris=[]
    for shape,col in objects: tris+=shape_triangles(shape,col)
    eye=np.array(camera,float); eye/=np.linalg.norm(eye)
    right=np.cross([0.,0.,1.],eye); right/=np.linalg.norm(right)
    up=np.cross(eye,right)
    proj=np.column_stack([right,-up,eye])
    raw=np.concatenate([t@proj for t,c in tris])
    low=raw[:,:2].min(axis=0); high=raw[:,:2].max(axis=0)
    scale=min((size[0]-130)/(high[0]-low[0]),(size[1]-130)/(high[1]-low[1]))
    offset=np.array(size)/2-(high+low)/2*scale
    im=Image.new('RGB',size,(244,244,240)); d=ImageDraw.Draw(im)
    light=np.array([-.4,-.6,1.]); light/=np.linalg.norm(light)
    # Depth-buffered triangles prevent a screen or rear rail drawing through another solid.
    pix=np.asarray(im).copy(); zbuf=np.full((size[1],size[0]),-np.inf)
    for t,col in tris:
        normal=np.cross(t[1]-t[0],t[2]-t[0]); norm=np.linalg.norm(normal)
        if norm<1e-10: continue
        normal/=norm
        q=t@proj
        if np.dot(normal,eye)<-0.00001: continue
        xy=q[:,:2]*scale+offset
        x0=max(0,int(math.floor(xy[:,0].min()))); x1=min(size[0]-1,int(math.ceil(xy[:,0].max())))
        y0=max(0,int(math.floor(xy[:,1].min()))); y1=min(size[1]-1,int(math.ceil(xy[:,1].max())))
        if x1<x0 or y1<y0: continue
        yy,xx=np.mgrid[y0:y1+1,x0:x1+1]; xx=xx+.5; yy=yy+.5
        a,b,c=xy
        den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-9: continue
        u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
        v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den
        w=1-u-v; zz=u*q[0,2]+v*q[1,2]+w*q[2,2]
        mask=(u>=-1e-8)&(v>=-1e-8)&(w>=-1e-8)&(zz>zbuf[y0:y1+1,x0:x1+1])
        shade=.48+.52*max(0,float(np.dot(normal,light)))
        color=np.clip(np.array(col)*shade,0,255).astype(np.uint8)
        pix[y0:y1+1,x0:x1+1][mask]=color
        zbuf[y0:y1+1,x0:x1+1][mask]=zz[mask]
    return Image.fromarray(pix)
