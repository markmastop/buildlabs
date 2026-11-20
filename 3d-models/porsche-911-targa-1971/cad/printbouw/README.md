# De Targa-printset opnieuw bouwen

De geometrie komt uit de [actuele projectpagina](../../index.html). De viewer rekent intern met millimeters op ware grootte. De export zet de lokale autocoördinaten om naar millimeters op schaal 1:10, met de neus langs positieve X en boven langs positieve Z. De referentiefoto’s zijn tijdens het bouwen overbodig. De oude Blender-studie is een afzonderlijk ontwerp.

## Bronnen en gereedschap

- `lees-viewer.cjs` leest de driehoeken uit de Three.js-scène. De kleurcode van de hoofdmesh onderscheidt de buitenhuid van de visuele vloer en wielkasten. Verborgen dakgeometrie wordt meegenomen. De vier commerciële kitwielen en het M-06-referentiechassis horen bij de viewer.
- `huid.py` berekent de afstand tot de modeloppervlakken en maakt er gesloten wanden van. `bouw.py` bevat de wanddiktes, passingen, asdragers en plaatstanden. De pasveer en de sleuf zijn afzonderlijk bemaat.
- STL en 3MF bevatten dezelfde driehoeken in de opgegeven printstand. De STEP-bestanden zijn gefacetteerde solids in montagepositie. De CAD-export vereenvoudigt de oppervlakken tot een tolerantie van 0,19 mm. Pas de bronparameters aan voor een andere schaal, wand of maatpassing.

## Uitvoeren

Werk vanuit de projectmap. Gebruik Python 3.11, Node.js en Playwright met Chromium. De slicercontrole gebruikt de macOS-versie van Bambu Studio met de BBL-profielen voor de P2S. Gebruik voor een geïnstalleerde Chrome eventueel de omgevingsvariabele `CHROME_BIN`. Een offline-kopie van Three.js r128 en de bijbehorende OrbitControls kan via `THREE_R128` en `ORBIT_R128` worden doorgegeven.

```sh
python3.11 -m venv .venv
.venv/bin/pip install -r cad/printbouw/requirements.txt
npm install --prefix .venv/browser playwright
.venv/browser/node_modules/.bin/playwright install chromium
werkmap=$(mktemp -d)
NODE_PATH="$PWD/.venv/browser/node_modules" node cad/printbouw/lees-viewer.cjs "$werkmap"
.venv/bin/python cad/printbouw/bouw.py "$werkmap"
.venv/bin/python cad/printbouw/controle.py
.venv/bin/python cad/printbouw/slicecontrole.py
.venv/bin/python cad/printbouw/pakket.py
```

De bouw schrijft naar `print/stl/`, `print/3mf/` en `cad/step/`. De bestandscontrole opent de bestanden opnieuw. De slicer maakt tijdelijke gereedschapsbanen. De pakketstap controleert de geometrie- en slicerhashes vóór het samenstellen van de ZIP.
