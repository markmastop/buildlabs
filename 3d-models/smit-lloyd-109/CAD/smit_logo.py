"""SMIT relief from official vector artwork, fused to the tapered funnel.
Source: https://smit.com/media/0kjd0u4j/smitlogo.svg (retrieved 2026-11-05).
Placement, 36 mm frame width, 0.75 mm relief and frame line are prototype choices.
Artwork is the SMIT mark; no claim about the historical livery of this vessel.
"""
import math
import xml.etree.ElementTree as ET
import cadquery as cq
from fontTools.pens.basePen import BasePen
from fontTools.svgLib.path import parse_path

class Contours(BasePen):
    def __init__(self):
        super().__init__(None);self.loops=[];self.current=[]
    def _moveTo(self,p):self.current=[tuple(p)]
    def _lineTo(self,p):self.current.append(tuple(p))
    def _curveToOne(self,a,b,c):
        start=self.current[-1]
        n=max(5,math.ceil((math.dist(start,a)+math.dist(a,b)+math.dist(b,c))/.4))
        for k in range(1,n+1):
            t=k/n;u=1-t
            self.current.append(tuple(u**3*start[j]+3*u*u*t*a[j]+3*u*t*t*b[j]+t**3*c[j] for j in [0,1]))
    def _qCurveToOne(self,a,b):
        start=self.current[-1]
        for k in range(1,17):
            t=k/16;u=1-t
            self.current.append(tuple(u*u*start[j]+2*u*t*a[j]+t*t*b[j] for j in [0,1]))
    def _closePath(self):
        if math.dist(self.current[0],self.current[-1])<1e-7:self.current.pop()
        self.loops.append(self.current);self.current=[]
    def _endPath(self):self._closePath()

def artwork(svgfile):
    loops=[]
    for el in ET.parse(svgfile).getroot():
        tag=el.tag.split('}')[-1];kind=el.get('class')
        if kind not in ['cls-2','cls-3']:continue
        if tag=='polygon':
            coords=el.get('points').replace(',',' ').split();loops.append([(float(coords[i]),float(coords[i+1])) for i in range(0,len(coords),2)])
        elif tag=='rect':
            x,y,w,h=[float(el.get(k)) for k in ['x','y','width','height']];loops.append([(x,y),(x+w,y),(x+w,y+h),(x,y+h)])
        elif tag=='path':
            pen=Contours();parse_path(el.get('d'),pen);loops.extend(pen.loops)
    assert len(loops)==8,len(loops)
    return loops

def relief(svgfile,sign,width=36,height_center=125,depth=.75,x_center=280,y_center=None,z_bottom=50,base_width=44,top_width=30,total_height=134):
    scale=width/58.82;cx=.5+58.82/2;cy=.48+72.12/2
    def convert(loop):return [((cx-x)*scale,(cy-y)*scale) for x,y in loop]
    def wire(loop,z,drop=0):
        return cq.Workplane('XY').polyline([(x,y-drop) for x,y in loop]).close().wire().val().translate(cq.Vector(0,0,z))
    # A 0.6 mm shear below the top profile provides a 45-degree ramp at lower edges.
    def raised(loop):
        return cq.Solid.makeLoft([wire(loop,-.18,.6),wire(loop,.42),wire(loop,depth)],ruled=True)
    loops=[convert(p) for p in artwork(svgfile)]
    reliefs=[raised(p) for p in loops]
    outer=[(-width/2,-72.12*scale/2),(width/2,-72.12*scale/2),(width/2,72.12*scale/2),(-width/2,72.12*scale/2)]
    inner=[(-width/2+.8,-72.12*scale/2+.8),(width/2-.8,-72.12*scale/2+.8),(width/2-.8,72.12*scale/2-.8),(-width/2+.8,72.12*scale/2-.8)]
    reliefs.append(raised(outer).cut(raised(inner)))
    slope=(base_width-top_width)/2/total_height;norm=math.sqrt(1+slope*slope)
    if y_center is None:y_center=sign*77.5
    origin=(x_center,y_center+sign*(base_width/2-(height_center-z_bottom)*slope),height_center)
    # Local U points right as seen from outside each side: both wordmarks read normally.
    plane=cq.Plane(origin=origin,xDir=(-sign,0,0),normal=(0,sign/norm,slope/norm))
    compound=cq.Compound.makeCompound(reliefs)
    return cq.Workplane(obj=compound.transformShape(plane.rG))

def add_logo(funnel,svgfile,sign):
    logo=relief(svgfile,sign)
    old=funnel.val().Volume()
    result=funnel.union(logo,clean=True)
    assert len(result.solids().vals())==1,'Logo must be fused to funnel wall'
    assert result.val().isValid(),'Invalid fused funnel'
    assert result.val().Volume()>old,'Relief did not increase material volume'
    return result
