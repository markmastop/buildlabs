"""Zelfstandige viewer rechtstreeks uit de gevalideerde printmeshes.
Geen tweede CAD-tessellatie, dus exact dezelfde kleine details als de STL/3MF.
"""
import json,math
from pathlib import Path
import numpy as np
import trimesh


def create_viewer(root,records):
 root=Path(root);data=[];cache={};rows={q['name']:q for q in records}
 def local(name):
  if name not in cache:
   q=rows[name];m=trimesh.load_mesh(root/'print/stl'/(name+'.stl'),process=True)
   m.apply_translation(-np.array(q['bed_translation']))
   if q['rotation']:
    axis,angle=q['rotation'];m.apply_transform(trimesh.transformations.rotation_matrix(-math.radians(angle),axis))
   cache[name]=m
  return cache[name]
 def emit(label,name,translation,color,group):
  m=local(name);v=m.vertices+translation;v=v[:,[0,2,1]]*np.array([1,1,-1])
  data.append(dict(name=label,color=color,group=group,vertices=np.round(v,4).tolist(),faces=m.faces.tolist()))
 for q in records:
  if q['included']:
   for i,p in enumerate(q['assembly_translations']):emit(q['name']+'_'+str(i+1),q['name'],p,q['color'],q['group'])
 for i,y in enumerate([-32,32]):
  for name in ['60_heli_romp_BB','60_heli_romp_SB','61_heli_landingsgestel']+[n for n in rows if n.startswith('64_heli_ruit_')]:
   emit(name+'_'+str(i),name,[213,y,168.1],rows[name]['color'],'heli')
  emit('heli_staartrotor_'+str(i),'63_heli_staartrotor',[279.65,y+2.5,179.1],'#242b30','heli')
 for y in [-69,69]:
  for k in range(3):emit('opgeborgen_rotor_'+str(y)+'_'+str(k),'62_heli_rotorblad',[196.05,y,139.4+k*1.2],'#242b30','bovenbouw')
 template=(root/'cad/viewer-template.html').read_text()
 (root/'cad/index.html').write_text(template.replace('/*MODEL_DATA*/[]',json.dumps(data,separators=(',',':'))))
 print('CAD-viewer: '+str(len(data))+' meshes uit de echte STL-bestanden',flush=True)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1]
 create_viewer(root,json.loads((root/'print/onderdelen.json').read_text())['parts'])
