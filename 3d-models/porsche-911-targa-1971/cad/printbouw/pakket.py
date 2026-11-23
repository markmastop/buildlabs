"""Bundel alleen de actuele export, de bron, de instructies en gecontroleerde profielen."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
from bestanden import zip_entry

ROOT=Path(__file__).resolve().parents[2]
PRINT=ROOT/'print'
checks=json.loads((PRINT/'controle.json').read_text())
slices=json.loads((PRINT/'slicercontrole.json').read_text())
assert checks['status']==slices['status']=='PASS'
digest=lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
parts=json.loads((PRINT/'onderdelen.json').read_text())
names=[p['name'] for p in parts]
assert names==[p['part'] for p in checks['parts']]==[p['part'] for p in slices['checks']]
files=[ROOT/'index.html',ROOT/'README.md',ROOT/'concept/ontwerpvoorstel.png',
       PRINT/'README.md',PRINT/'montage-asdrager.png',PRINT/'onderdelen.json',PRINT/'onderdelen.csv',
       PRINT/'controle.json',PRINT/'slicercontrole.json',PRINT/'profielen/targa-p2s.json',
       PRINT/'profielen/targa-kleine-overhangen-p2s.json']
files.extend(sorted(p for p in (ROOT/'cad/printbouw').iterdir() if p.is_file() and p.suffix in {'.md','.txt','.py','.cjs'}))
for row,sl in zip(checks['parts'],slices['checks']):
    n=row['part']
    for kind,path in [('stl',PRINT/'stl'/(n+'.stl')),('three_mf',PRINT/'3mf'/(n+'.3mf')),
                      ('step',ROOT/'cad/step'/(n+'.step'))]:
        assert digest(path)==row[kind+'_sha256']
        if kind=='three_mf': assert digest(path)==sl['sha256']
        files.append(path)
assembly=ROOT/'cad/step/targa-v7-assemblage.step'
assert digest(assembly)==checks['assembly_sha256']
files.append(assembly)
sums=PRINT/'SHA256SUMS.txt'
sums.write_text(''.join(f'{digest(f)}  {f.relative_to(ROOT)}\n' for f in sorted(files)))
files.append(sums)
dest=ROOT/'911-targa-1971-v7-printpakket.zip'
with ZipFile(dest,'w') as z:
    for f in sorted(files):zip_entry(z,str(f.relative_to(ROOT)),f.read_bytes())
with ZipFile(dest) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(files))
print(dest,len(files),'bestanden',round(dest.stat().st_size/1e6,1),'MB')
