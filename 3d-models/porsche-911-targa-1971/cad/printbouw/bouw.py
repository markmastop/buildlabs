"""Bouw de pasproef en de 1:10-printdelen uit de geëxporteerde Three.js-scène."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import manifold3d as mf
import trimesh
from huid import surface, regularize
from bestanden import export_print, export_step

ROOT=Path(__file__).resolve().parents[2]
PRINT=ROOT/'print'
STEP=ROOT/'cad'/'step'
SPLIT=-26.
SOCKET_Y=69.5
SOCKET_Z=37.
GLUE_GAP=.22
M=mf.Manifold


def box(center,size):
    return M.cube(size,True).translate(center)


def one(part,label,min_volume=2.):
    """Verwijder uitsluitend kleine fragmenten die binnen de snijspeling vallen."""
    components=sorted(part.decompose(),key=lambda s:-s.volume())
    if not components or part.status()!=mf.Error.NoError:
        raise ValueError((label,part.status()))
    if sum(abs(c.volume()) for c in components[1:])>min_volume:
        raise ValueError((label,[(round(c.volume(),2),c.bounding_box()) for c in components[:8]]))
    return components[0]


def maak_step(parts):
    assembly=[]
    for p in parts:
        name=p['name']
        stl=trimesh.load_mesh(PRINT/'stl'/(name+'.stl'))
        exact=M(mf.Mesh64(np.asarray(stl.vertices,np.float64),np.asarray(stl.faces,np.uint64)))
        exact=exact.translate(p['rotated_origin_mm']).rotate(-np.array(p['assembly_to_bed_rotation_deg']))
        cad=one(exact.as_original().simplify(.19),name+' STEP')
        # Bij dunne panelen kan een kleine facettering de wand merkbaar verdunnen.
        if abs(cad.volume()/exact.volume()-1)>.015:
            cad=exact
        export_step(STEP/(name+'.step'),[(name,cad)])
        if p['group']!='proef':
            assembly.append((name,cad))
            if p['mirror_y_copy']:
                assembly.append((name+'-2',cad.mirror((0,1,0))))
    export_step(STEP/'targa-assemblage.step',assembly)


def main(work):
    for folder in (PRINT/'3mf',PRINT/'stl',STEP):
        folder.mkdir(parents=True,exist_ok=True)
    def triangles(name):
        return np.fromfile(work/(name+'.tri'),'<f4').reshape(-1,3,3).astype(float)
    def shell(spec,pitch):
        return surface([(triangles(n),r) for n,r in spec],pitch)
    def skin(extra=0):
        return one(shell([('huid',.96+extra),('details',.70+extra)],.46),'carrosserie')
    body=skin()
    clearance=skin(GLUE_GAP)
    # Negatieve naden liggen aan de buitenzijde. De binnenwand blijft doorlopen.
    door=triangles('deurnaden'); door[:,:,1]+=.85*np.sign(door[:,:,1])
    lids=triangles('klepnaden'); lids[:,:,2]+=.85
    body=body-surface([(door,.29),(lids,.27)],.30)
    body=one(regularize(body,.36),"laknaden")
    keybox=(22.,6.4,9.)
    bore=(18.,2.5,5.5)
    key=box((SPLIT,SOCKET_Y,SOCKET_Z),(17.,2.,5.))
    for sign in (-1,1):
        center=(SPLIT,sign*SOCKET_Y,SOCKET_Z)
        boss=box(center,keybox)
        body=(body+boss)-box(center,bore)
        clearance=clearance+boss
    front,rear=body.split_by_plane((1,0,0),SPLIT)
    coupon=box((0,0,0),keybox)-box((0,0,0),bore)
    coupon=coupon.trim_by_plane((1,0,0),0)
    parts=[]
    def add(name,shape,rotation=(0,0,0),quantity=1,group='model',mirror_copy=False):
        part=one(shape,name).as_original().set_tolerance(.001).simplify(.07)
        oriented=part.rotate(rotation)
        origin=oriented.bounding_box()[:3]
        oriented=oriented.translate(tuple(-v for v in origin))
        if max(np.subtract(oriented.bounding_box()[3:],oriented.bounding_box()[:3]))>246:
            raise ValueError(name+' overschrijdt de bruikbare plaatmaat')
        print(name,part.num_tri(),round(part.volume()/1000,1),'cm3',flush=True)
        parts.append((name,oriented,quantity,group,mirror_copy,rotation,origin))
    add('00-pasblok',coupon,(0,90,0),2,'proef')
    add('01-pasveer',key,(90,0,0),quantity=2,mirror_copy=True)
    add('02-carrosserie-voor',front,(0,-90,0))
    add('03-carrosserie-achter',rear,(0,90,0))
    # Een vrije instap van onderaf. Vier lijmoren raken de binnenzijde van de dorpels.
    interior=shell([('interieur',.70)],.34)
    trunk,left,right=sorted(interior.decompose(),key=lambda p:-p.volume())
    seats=sorted([left,right],key=lambda p:p.bounding_box()[1],reverse=True)
    for sign in (-1,1):
        for x in (-43.,19.):
            trunk=trunk+box((x,sign*64.,34.15),(10.,18.,2.1))
    # Bewegingsruimte boven de achterbanden van zowel de kit als de vitrineversie.
    for y in (-70.,70.):
        envelope=M.cylinder(31.,34.5,34.5,96,True).rotate((90,0,0)).translate((-113.4,y,32.2))
        trunk=trunk-envelope
    trunk=one(trunk-clearance,'interieurbak')
    add('04-interieurbak',regularize(trunk,.30))
    for sign,seat,label in zip((1,-1),seats,('links','rechts')):
        # Twee rails vormen vlakke lijmvoeten op de vloer.
        for y in (23.,39.):
            seat=seat+box((-22.,sign*y,38.45),(24.,3.2,7.7))
        add('05-voorstoel-'+label,seat-trunk)
    roof=shell([('dak',.55)],.27).translate((0,0,.70))
    add('06-targadak',roof-clearance)
    panes={}
    for name,offset in [('voorruit',(-1.20,0,-.85)),('achterruit',(1.05,0,-.85)),
                        ('tochtruit-links',(0,-1.1,0)),('tochtruit-rechts',(0,1.1,0))]:
        blank=shell([(name,.62)],.27).translate(offset)
        pane=one(blank-clearance,name)
        pane=one(regularize(pane,.24,.045),name)
        panes[name]=pane
        # Op de onderste rand; het gebogen buitenvlak blijft vrij van het bed.
        add('07-'+name,pane)
    mirror=shell([('binnenspiegel',.52)],.24).translate((-1.20,0,-.85))
    add('08-binnenspiegel',mirror-panes['voorruit'],(0,90,0))
    for name,x in [('wiel-voor',113.4),('wiel-achter',-113.4)]:
        wheel=shell([(name,.53)],.27)
        # Decoratieve 3-mm-as. De naaf stopt achter de vijf spaakvensters.
        inside=-58.35 if x>0 else -58.45
        hub=M.cylinder(15.,4.4,4.4,48).rotate((90,0,0)).translate((x,inside,32.2))
        void=M.cylinder(13.,1.60,1.60,48).rotate((90,0,0)).translate((x,inside+1.,32.2))
        wheel=one((wheel+hub)-void,name)
        add('09-fuchs'+('-voor' if x>0 else '-achter'),wheel,(-90,0,0),2,mirror_copy=True)
    exhaust=shell([('uitlaat',.53)],.27)
    for y in (-33.,33.):
        foot=box((-178.,y,27.),(4.,5.,4.))
        pad=box((-204.,y,39.5),(3.,7.,5.))
        exhaust=exhaust+M.batch_hull([foot,pad])
    # Behoud het binnenste segment van de steunen tot aan de achterwand.
    cut=sorted((exhaust-clearance).decompose(),key=lambda p:-p.volume())
    assert all(p.bounding_box()[3]<-196 and p.volume()<300 for p in cut[1:])
    add('10-uitlaat',cut[0])
    for axle,deck,label in [(113.4,113.4,'voor'),(-113.4,-157.,'achter')]:
        beam=box((axle,0,32.2),(9.,93.,8.))
        for y in (-40.,40.):
            hit=body.ray_cast((deck,y,40.),(deck,y,130.))[0].position[2]
            heel=box((axle,y,33.),(7.,6.,4.))
            pad=box((deck,y,hit-.5),(12.,8.,3.2))
            # De steun eindigt aan de binnenkant van de klep.
            top=body.ray_cast((deck,y,130.),(deck,y,40.))[0].position[2]
            upright=box((deck,y,33.),(7.,6.,4.))
            post=(M.batch_hull([heel,upright])+M.batch_hull([upright,pad]))-clearance
            post=max(post.decompose(),key=lambda q:q.volume())
            assert post.bounding_box()[5]<top+1.
            beam=beam+post
        bore=M.cylinder(100.,1.65,1.65,48).rotate((90,0,0)).translate((axle,50.,32.2))
        carrier=beam-bore
        assert (carrier^trunk).volume()<.5,(label,'asdrager raakt de interieurbak')
        add('11-asdrager-'+label,carrier)
    report=[]
    for name,oriented,qty,group,mirror_copy,rotation,origin in parts:
        export_print(PRINT,name,oriented)
        bb=np.array(oriented.bounding_box()).reshape(2,3)
        report.append(dict(name=name,quantity=qty,group=group,print_mm=np.round(bb[1]-bb[0],2).tolist(),
                           assembly_to_bed_rotation_deg=rotation,rotated_origin_mm=list(origin),
                           mirror_y_copy=mirror_copy,volume_cm3=round(oriented.volume()/1000,3)))
    maak_step(report)
    (PRINT/'onderdelen.json').write_text(json.dumps(report,indent=2)+'\n')
    with (PRINT/'onderdelen.csv').open('w') as f:
        writer=csv.writer(f,lineterminator="\n");writer.writerow(['onderdeel','aantal','groep','x_mm','y_mm','z_mm','volume_cm3'])
        for p in report:writer.writerow([p['name'],p['quantity'],p['group'],*p['print_mm'],p['volume_cm3']])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('werkmap',type=Path,help='Map met de .tri-bestanden uit lees-viewer.cjs')
    main(parser.parse_args().werkmap)
