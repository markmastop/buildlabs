"""Open uitwisselformaten. STL en 3MF delen dezelfde posities en driehoeken."""
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import numpy as np
import trimesh


def zip_entry(archive, name, data):
    info = ZipInfo(name, (2026, 1, 1, 0, 0, 0))
    archive.writestr(info, data, compress_type=ZIP_DEFLATED)


def export_print(directory, name, part):
    mesh = part.to_mesh()
    vertices, faces = mesh.vert_properties[:,:3], mesh.tri_verts
    stl = trimesh.Trimesh(vertices, faces, process=False)
    stl.export(directory/'stl'/(name+'.stl'))
    x,y = 128-stl.bounds.mean(axis=0)[:2]
    model = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<model unit="millimeter" xml:lang="nl-NL" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">',
             f'<resources><object id="1" type="model" name="{escape(name)}"><mesh><vertices>']
    model.extend('<vertex x="%.9g" y="%.9g" z="%.9g"/>' % tuple(v) for v in vertices)
    model.append('</vertices><triangles>')
    model.extend('<triangle v1="%d" v2="%d" v3="%d"/>' % tuple(f) for f in faces)
    model.extend(['</triangles></mesh></object></resources>',
                  f'<build><item objectid="1" transform="1 0 0 0 1 0 0 0 1 {x:.6f} {y:.6f} 0"/></build></model>'])
    with ZipFile(directory/'3mf'/(name+'.3mf'),'w') as z:
        zip_entry(z,'3D/3dmodel.model','\n'.join(model))
        zip_entry(z,'[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        zip_entry(z,'_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rel0" Target="/3D/3dmodel.model" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')


def export_step(path, shapes):
    """FACETED_BREP in millimeters, met gedeelde hoekpunten en benoemde solids."""
    with Path(path).open('w') as stream:
        stream.write("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('Targa 1:10'),'2;1');\n"
                     "FILE_NAME('targa.step','2026-11-20T00:00:00',('Build Labs'),('Build Labs'),'printbouw','Build Labs','');\n"
                     "FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));\nENDSEC;\nDATA;\n")
        counter=0
        def put(entity):
            nonlocal counter
            counter+=1
            stream.write(f'#{counter}={entity};\n')
            return counter
        def refs(ids):
            return ','.join(f'#{i}' for i in ids)
        app=put("APPLICATION_CONTEXT('automotive design')")
        put(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#{app})")
        pc=put(f"PRODUCT_CONTEXT('',#{app},'mechanical')")
        product=put(f"PRODUCT('Targa','Targa','',(#{pc}))")
        form=put(f"PRODUCT_DEFINITION_FORMATION('1','',#{product})")
        dc=put(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{app},'design')")
        definition=put(f"PRODUCT_DEFINITION('design','',#{form},#{dc})")
        shape=put(f"PRODUCT_DEFINITION_SHAPE('','',#{definition})")
        mm=put("(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.))")
        rad=put("(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.))")
        sr=put("(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT())")
        prec=put(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-6),#{mm},'distance_accuracy_value','')")
        ctx=put(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{prec})) GLOBAL_UNIT_ASSIGNED_CONTEXT((#{mm},#{rad},#{sr})) REPRESENTATION_CONTEXT('','3D'))")
        origin=put("CARTESIAN_POINT('',(0.,0.,0.))")
        axis=put(f"AXIS2_PLACEMENT_3D('',#{origin},$,$)")
        solids=[]
        for name,part in shapes:
            mesh=part.to_mesh64()
            vertices=[]
            for v in mesh.vert_properties[:,:3]:
                xyz=','.join(f'{coord:.8f}' for coord in v)
                vertices.append(put(f"CARTESIAN_POINT('',({xyz}))"))
            faces=[]
            coords=mesh.vert_properties[:,:3].astype(np.float64)
            tris=coords[mesh.tri_verts]
            normals=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0])
            lengths=np.linalg.norm(normals,axis=1)
            assert lengths.min()>1.e-14,(name,"nulvlak")
            normals/=lengths[:,None]
            axes=tris[:,1]-tris[:,0]
            axes/=np.linalg.norm(axes,axis=1)[:,None]
            for (a,b,c),normal,tangent in zip(mesh.tri_verts,normals,axes):
                loop=put(f"POLY_LOOP('',(#{vertices[a]},#{vertices[b]},#{vertices[c]}))")
                bound=put(f"FACE_OUTER_BOUND('',#{loop},.T.)")
                directions=[]
                for vec in (normal,tangent):
                    xyz=','.join(f'{value:.10f}' for value in vec)
                    directions.append(put(f"DIRECTION('',({xyz}))"))
                axis3=put(f"AXIS2_PLACEMENT_3D('',#{vertices[a]},#{directions[0]},#{directions[1]})")
                plane=put(f"PLANE('',#{axis3})")
                faces.append(put(f"FACE_SURFACE('',(#{bound}),#{plane},.T.)"))
            shell=put(f"CLOSED_SHELL('',({refs(faces)}))")
            solids.append(put(f"FACETED_BREP('{name}',#{shell})"))
        rep=put(f"FACETED_BREP_SHAPE_REPRESENTATION('',({refs([axis,*solids])}),#{ctx})")
        put(f"SHAPE_DEFINITION_REPRESENTATION(#{shape},#{rep})")
        stream.write('ENDSEC;\nEND-ISO-10303-21;\n')
