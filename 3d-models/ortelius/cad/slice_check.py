"""Proefslicen met lokale Bambu Studio, zonder te printen of G-code te publiceren.
python cad/slice_check.py [deelnaam ...]; standaard alle unieke onderdelen.
"""
from pathlib import Path
import json,subprocess,tempfile,sys,hashlib
R=Path(__file__).resolve().parents[1]
APP=Path('/Applications/BambuStudio.app/Contents')
BIN=APP/'MacOS/BambuStudio';PROFILES=APP/'Resources/profiles/BBL'
D=json.loads((R/'print/onderdelen.json').read_text())
previous_path=R/'print/slicercontrole.json'
previous=json.loads(previous_path.read_text()) if previous_path.exists() else {}
checks=[];tmp=Path(tempfile.mkdtemp(prefix='ortelius-p2-slice-'))
# De CLI lost inherits/include niet vanzelf op: maak tijdelijke volledige profielen.
lookup={p.stem:p for p in PROFILES.rglob('*.json')}
def resolve(path):
 d=json.loads(path.read_text());out={}
 if d.get('inherits'):out.update(resolve(lookup[d['inherits']]))
 for inc in d.get('include',[]):out.update(resolve(lookup[inc]))
 out.update(d);out.pop('inherits',None);out.pop('include',None)
 return out
machine=resolve(PROFILES/'machine/Bambu Lab P2S 0.4 nozzle.json')
machine['curr_bed_type']='Textured PEI Plate'
assert machine['printable_height']=='256'
assert any('256' in s for s in machine['printable_area'])
# PETG (zie ONTWERP.md). Profielnamen verschillen per Bambu Studio-versie: neem de eerste die bestaat.
FILAMENTS=['Generic PETG @BBL P2S','Generic PETG HF @BBL P2S','Generic PETG @BBL X1C','Generic PETG']
name=next((n for n in FILAMENTS if (PROFILES/'filament'/(n+'.json')).exists()),None)
assert name,('Geen PETG-profiel gevonden in '+str(PROFILES/'filament'),FILAMENTS)
filament=resolve(PROFILES/'filament'/(name+'.json'))
for n,d in [('machine',machine),('filament',filament)]:
 (tmp/(n+'.json')).write_text(json.dumps(d))
for n in ['romp','details']:
 path=R/'print/profielen'/('ortelius-p2-'+n+'-p2s.json')
 d=resolve(path);d['curr_bed_type']='Textured PEI Plate'
 (tmp/(n+'.json')).write_text(json.dumps(d))
selected=set(sys.argv[1:])
assert selected.issubset({q['name'] for q in D['parts']}),'Onbekende onderdeelnamen'
for q in D['parts']:
 name=q['name']
 if selected and name not in selected:continue
 folder=tmp/name;folder.mkdir();profile='romp' if q['group'] in ['romp','proef'] else 'details'
 cmd=[str(BIN),'--load-settings',str(tmp/'machine.json')+';'+str(tmp/(profile+'.json')),'--load-filaments',str(tmp/'filament.json'),'--ensure-on-bed','--arrange','0','--orient','0','--slice','0','--outputdir',str(folder),str(R/'print/3mf'/(name+'.3mf'))]
 with (folder/'cli.log').open('w') as log:
  p=subprocess.run(cmd,cwd=tmp,stdout=log,stderr=subprocess.STDOUT,timeout=180)
 path=folder/'result.json';result=json.loads(path.read_text()) if path.exists() else {}
 assert p.returncode==0 and result.get('return_code')==0,(name,p.returncode,result,(folder/'cli.log').read_text()[-2000:])
 assert result['wall_loops']==(6 if profile=='romp' else 4),(name,'profiel niet toegepast',result['wall_loops'])
 assert abs(result['layer_height']-(.20 if profile=='romp' else .16))<.001
 plates=result.get('sliced_plates',[]);assert len(plates)==1
 plate=plates[0]
 if plate.get('objects'):assert plate['objects'][0]['bbox']['height']<=246.01
 assert max(q['print_mm'])<=246.01
 grams=sum(f.get('total_used_g',0) for f in plate.get('filaments',[]))
 assert grams>0,(name,'filamentprofiel ontbreekt')
 checks.append(dict(part=name,profile=profile,status='PASS',warning=plate.get('warning_message',''),wall_loops=result['wall_loops'],layer_height_mm=round(result['layer_height'],2),estimated_grams=round(grams,2),estimated_seconds=round(plate['total_predication']),source_3mf_sha256=hashlib.sha256((R/'print/3mf'/(name+'.3mf')).read_bytes()).hexdigest()))
 print(name,'SLICE OK',checks[-1]['estimated_grams'],'g',flush=True)
 report=dict(revision=D['revision'],slicer='Bambu Studio 02.09.01.70 macOS CLI',printer=machine['printer_model'],nozzle_mm=.4,bed_mm=[256,256,256],filament=filament['name'],status='RUNNING',scope='Alle unieke onderdelen, 1 exemplaar per plaat' if not selected else 'Geselecteerde onderdelen',checks=checks,temporary_gcode_directory=str(tmp),limitations='Proefslicing, geen fysieke proef. Ondersteuning en hechting visueel beoordelen vóór productie.')
 (R/'print/slicercontrole.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# Reeds geslaagde controles alleen hergebruiken als geometrie én alle
# opgeloste printer-/proces-/filamentinstellingen exact overeenkomen.
if selected and previous.get('status')=='PASS':
 olddir=Path(previous.get('temporary_gcode_directory','/nonexistent'))
 settings=['machine.json','filament.json','romp.json','details.json']
 same_settings=all((olddir/f).exists() and json.loads((olddir/f).read_text())==json.loads((tmp/f).read_text()) for f in settings)
 old={q['part']:q for q in previous.get('checks',[])}
 fresh={q['part']:q for q in checks}
 if same_settings and all(q['name'] in old and old[q['name']]['source_3mf_sha256']==hashlib.sha256((R/'print/3mf'/(q['name']+'.3mf')).read_bytes()).hexdigest() for q in D['parts'] if q['name'] not in selected):
  combined=[]
  for q in D['parts']:
   name=q['name']
   if name in fresh:combined.append(fresh[name])
   else:combined.append(dict(old[name],reused_verified_mesh=True))
  checks=combined;report['checks']=checks
  report['scope']='Alle actuele unieke onderdelen; '+str(len(selected))+' opnieuw gesliced, overige byte-identieke meshes met identieke opgeloste instellingen hergebruikt.'
  report['reused_settings_directory']=str(olddir)
report['status']='PASS'

report['expected_unique_parts']=len(D['parts'])
quantities={q['name']:q['quantity'] for q in D['parts']}
report['complete_print_list_estimate_g']=round(sum(q['estimated_grams']*quantities[q['part']] for q in checks),1)
report['complete_print_list_estimate_hours']=round(sum(q['estimated_seconds']*quantities[q['part']] for q in checks)/3600,1)
(R/'print/slicercontrole.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('SLICER PASS',len(checks),'onderdelen',flush=True)
