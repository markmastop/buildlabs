"""Lees de opgeleverde bestanden terug, inclusief hun plaat- en montagematen."""
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import hashlib
import json
import re
from itertools import combinations
import manifold3d as mf

import cadquery as cq
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[2]
PRINT=ROOT/'print'
STEP=ROOT/'cad/step'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(part):
    name=part['name']
    stl=PRINT/'stl'/(name+'.stl')
    three=PRINT/'3mf'/(name+'.3mf')
    step=STEP/(name+'.step')
    mesh=trimesh.load_mesh(stl,process=True)
    assert mesh.is_watertight and mesh.is_volume and mesh.body_count==1,(name,mesh.is_watertight,mesh.euler_number,mesh.body_count)
    assert np.allclose(mesh.extents,part['print_mm'],atol=.006) and max(mesh.extents)<246
    assert abs(mesh.bounds[0,2])<.001 and abs(mesh.volume/1000-part['volume_cm3'])<.002
    with ZipFile(three) as pack:
        assert not pack.testzip()
        model=ET.fromstring(pack.read('3D/3dmodel.model'))
    assert model.get('unit')=='millimeter'
    verts=np.array([[v.get(k) for k in ('x','y','z')] for v in model.findall('.//{*}vertex')],dtype=np.float32)
    tris=np.array([[t.get(k) for k in ('v1','v2','v3')] for t in model.findall('.//{*}triangle')],dtype=np.uint32)
    # Vergelijk dezelfde driehoeken rechtstreeks, inclusief de winding.
    original=trimesh.load_mesh(stl,process=False)
    assert np.array_equal(verts[tris],original.triangles.astype(np.float32)),name
    item=model.find('.//{*}item')
    matrix=np.fromstring(item.get('transform'),sep=' ').reshape(4,3)
    on_plate=verts@matrix[:3]+matrix[3]
    assert on_plate.min(axis=0)[:2].min()>5 and on_plate.max(axis=0)[:2].max()<251
    solid=cq.importers.importStep(str(step)).val()
    solids=solid.Solids()
    assert len(solids)==1,(name,'STEP solids',len(solids))
    assert solids[0].isValid(),(name,'ongeldig STEP-solid')
    volume=solids[0].Volume()
    assert volume>0 and abs(volume/mesh.volume-1)<.035,(name,'STEP-volume',volume,mesh.volume)
    print(name,'STL/3MF/STEP',len(mesh.faces),'driehoeken',flush=True)
    return dict(part=name,status='PASS',triangles=len(mesh.faces),watertight=True,
                connected_components=mesh.body_count,step_solids=len(solids),step_valid=True,step_volume_cm3=round(volume/1000,3),
                stl_sha256=sha(stl),three_mf_sha256=sha(three),step_sha256=sha(step))


def assembly_contacts(parts):
    placed={}
    for p in parts:
        if p['group']=='proef':
            continue
        mesh=trimesh.load_mesh(PRINT/'stl'/(p['name']+'.stl'))
        shape=mf.Manifold(mf.Mesh64(np.asarray(mesh.vertices,np.float64),np.asarray(mesh.faces,np.uint64)))
        assert not shape.is_empty()
        # De plaatstanden hebben hoogstens één niet-nulle Eulerhoek.
        shape=shape.translate(p['rotated_origin_mm']).rotate(-np.array(p['assembly_to_bed_rotation_deg']))
        placed[p['name']]=shape
        if p['mirror_y_copy']:
            placed[p['name']+'-2']=shape.mirror((0,1,0))
    peak=0.
    for (name,a),(other,b) in combinations(placed.items(),2):
        lo,hi=np.array(a.bounding_box()).reshape(2,3)
        low,high=np.array(b.bounding_box()).reshape(2,3)
        if np.any(np.minimum(hi,high)-np.maximum(lo,low)<=.001):
            continue
        overlap=(a^b).volume()
        assert overlap<.5,(name,other,'overlap in mm3',overlap)
        peak=max(peak,overlap)
    return round(peak,4)


def main():
    parts=json.loads((PRINT/'onderdelen.json').read_text())
    checks=[audit(p) for p in parts]
    assembly=STEP/'targa-assemblage.step'
    labels=re.findall(r"FACETED_BREP\('([^']+)'",assembly.read_text())
    assert len(labels)==sum(p['quantity'] for p in parts if p['group']=='model')
    assert len(set(labels))==len(labels)
    compound=cq.importers.importStep(str(assembly)).val()
    assert len(compound.Solids())==len(labels) and compound.isValid()
    bounds=compound.BoundingBox()
    report=dict(assembly_valid=True,assembly_mm=[round(n,2) for n in (bounds.xlen,bounds.ylen,bounds.zlen)],
                status='PASS',units='mm',bed_mm=[256]*3,assembly_solids=len(labels),
                max_overlap_mm3=assembly_contacts(parts),assembly_sha256=sha(assembly),parts=checks)
    (PRINT/'controle.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()
