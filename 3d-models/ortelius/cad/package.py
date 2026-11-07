"""Maak een lokaal ZIP-pakket; gitignore houdt distributie-ZIP's buiten Git."""
from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'print/onderdelen.json').read_text())
C=json.loads((R/'print/controle.json').read_text())
S=json.loads((R/'print/slicercontrole.json').read_text())
assert C['status']=='PASS' and C['unique_parts']==len(D['parts'])
assert S['status']=='PASS' and len(S['checks'])==len(D['parts'])
assert {p['name'] for p in D['parts']}=={p['part'] for p in S['checks']}
for c in S['checks']:
 assert hashlib.sha256((R/'print/3mf'/(c['part']+'.3mf')).read_bytes()).hexdigest()==c['source_3mf_sha256'],c['part']
out=R/'ortelius-p2-printpakket.zip'
files=[]
for folder in ['cad','print','beelden']:
 files.extend(p for p in (R/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.extend(R/f for f in ['index.html','README.md','START-HIER.md','ONTWERP.md','ONDERDELEN.md','referentie/README.md'])
# Geen referentiefoto's, dependencies, credentials of G-code.
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(files):
  assert p.suffix.lower() not in ['.gcode','.bgcode','.pyc']
  z.write(p,'ortelius-p2/'+str(p.relative_to(R)))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(out,round(out.stat().st_size/1e6,2),'MB;',len(files),'bestanden')
