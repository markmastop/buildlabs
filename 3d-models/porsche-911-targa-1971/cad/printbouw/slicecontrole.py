"""Proefslice ieder uniek onderdeel in zijn 3MF-oriëntatie met Bambu Studio."""
import hashlib
import json
import os
from pathlib import Path
import plistlib
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[2]
PRINT=ROOT/'print'
APP=Path(os.environ.get('BAMBU_APP','/Applications/BambuStudio.app/Contents'))
PROFILES=APP/'Resources/profiles/BBL'
LOOKUP={p.stem:p for p in PROFILES.rglob('*.json')}


def resolve(path):
    profile=json.loads(path.read_text())
    result=resolve(LOOKUP[profile['inherits']]) if profile.get('inherits') else {}
    for parent in profile.get('include',[]):
        result.update(resolve(LOOKUP[parent]))
    result.update(profile)
    result.pop('inherits',None);result.pop('include',None)
    return result


def main():
    parts=json.loads((PRINT/'onderdelen.json').read_text())
    machine=resolve(LOOKUP['Bambu Lab P2S 0.4 nozzle'])
    material=resolve(LOOKUP['Generic PLA @BBL P2S'])
    general='targa-p2s'
    detail='targa-kleine-overhangen-p2s'
    version=plistlib.loads((APP/'Info.plist').read_bytes())['CFBundleShortVersionString']
    with tempfile.TemporaryDirectory(prefix='targa-p2s-') as tmp:
        work=Path(tmp)
        for name,data in [('machine',machine),('filament',material),(general,resolve(PRINT/'profielen'/(general+'.json'))),
                          (detail,resolve(PRINT/'profielen'/(detail+'.json')))]:
            (work/(name+'.json')).write_text(json.dumps(data))
        def check(part):
            name=part['name']; plate=work/name;plate.mkdir()
            model=PRINT/'3mf'/(name+'.3mf')
            profile=detail if name.startswith(('09-','10-','12-')) else general
            cmd=[str(APP/'MacOS/BambuStudio'),'--load-settings',str(work/'machine.json')+';'+str(work/(profile+'.json')),
                 '--load-filaments',str(work/'filament.json'),'--ensure-on-bed','--arrange','0','--orient','0',
                 '--slice','0','--outputdir',str(plate),str(model)]
            with (plate/'studio.log').open('w') as log:
                result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,cwd=plate,timeout=900)
            if result.returncode:
                raise ValueError((name,(plate/'studio.log').read_text()[-2200:]))
            data=json.loads((plate/'result.json').read_text())
            assert data['return_code']==0 and len(data['sliced_plates'])==1
            assert data['wall_loops']==3 and abs(data['layer_height']-.20)<.001
            info=data['sliced_plates'][0]
            grams=sum(f['total_used_g'] for f in info['filaments'])
            assert grams>0
            print(name,'gesliced',round(grams,1),'g',flush=True)
            assert not info.get('warning_message'),(name,info.get('warning_message'))
            return dict(part=name,profile=profile,grams=round(grams,2),seconds=round(info['total_predication']),
                        warning=info.get('warning_message',''),sha256=hashlib.sha256(model.read_bytes()).hexdigest())
        with ThreadPoolExecutor(max_workers=2) as pool:
            checks=list(pool.map(check,parts))
    report=dict(status='PASS',slicer='Bambu Studio '+version,printer=machine['printer_model'],filament=material['name'],
                nozzle_mm=.4,layer_mm=.2,checks=checks)
    for group in ('model','proef'):
        selected=[(c,p['quantity']) for c,p in zip(checks,parts) if p['group']==group]
        report[group]={'gram':round(sum(c['grams']*q for c,q in selected),1),
                       'uren':round(sum(c['seconds']*q for c,q in selected)/3600,1)}
    (PRINT/'slicercontrole.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()
