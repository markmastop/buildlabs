# Bewerkbare CAD — Ortelius p2

De parametrische bron is [`build.py`](build.py), met hoofdparameters in
[`parameters.json`](parameters.json). Eenheden zijn **millimeters**, schaal
1:100. Vormbron: de fotogebaseerde vormstudie v3 in [`../index.html`](../index.html).
P2 herstelt de details die in de eerste CAD-versie ontbraken. Raamstroken,
cockpitruiten, relingen en dekinleg zijn nu echte onderdelen. Touwen,
verstaging en kettingen blijven modelbouwwerk met draad.

## Bestanden

- [`index.html`](index.html): zelfstandige Three.js-viewer van de echte CAD-geometrie.
- [`step/ortelius-p2-assemblage.step`](step/ortelius-p2-assemblage.step): complete, benoemde STEP-assemblage.
- `step/`: bewerkbaar STEP per printonderdeel, in dezelfde printstand als het STL.
- [`build.py`](build.py): geometrie, deling, export en viewer-generatie.
- [`details.py`](details.py): echte relingen, trappen, masten, cockpitruiten en dekuitrusting.
- [`DETAILS.md`](DETAILS.md): vergelijking met de vormstudie en bewuste printaanpassingen.
- [`VERGELIJKING.md`](VERGELIJKING.md): silhouetvergelijking CAD tegen vormstudie, met de aanpassingen van 09-11.
- [`parameters.json`](parameters.json): rompstations, wanddiktes, lijmspeling, sneden en maatreserveringen.
- [`viewer.py`](viewer.py): bouwt de viewer rechtstreeks uit de georiënteerde STL-bestanden.
- [`viewer-template.html`](viewer-template.html): zelfstandige viewer met ingebedde modeldata.
- [`validate.py`](validate.py): onafhankelijke herimportcontrole, inclusief houders/romp en heli/hangar.
- [`slice_check.py`](slice_check.py): proefslicing met lokaal geïnstalleerde Bambu Studio op macOS.
- [`package.py`](package.py): maakt lokaal het ZIP-pakket, zonder dependencies of G-code.
- [`requirements.txt`](requirements.txt): vastgelegde Python-versies.

De overige scheepsmaten en detailvormen staan als leesbare parameters in de
Python-bron. STEP heeft bewerkbare BRep-geometrie; de parametrische
bouwgeschiedenis zit in Python en JSON, niet als Fusion/FreeCAD-featureboom.

## Opnieuw genereren

```sh
python3.11 -m venv /tmp/ortelius-cad
/tmp/ortelius-cad/bin/python -m pip install -r cad/requirements.txt
/tmp/ortelius-cad/bin/python cad/build.py
/tmp/ortelius-cad/bin/python cad/validate.py
/tmp/ortelius-cad/bin/python cad/slice_check.py
/tmp/ortelius-cad/bin/python cad/package.py
```

Voer dit uit vanuit de projectmap `ortelius/`. `slice_check.py` gebruikt de
P2S-profielen uit de lokale Bambu Studio-installatie; het lost profielerving
expliciet op en controleert of laaghoogte, zes/vier wanden en filament zijn
toegepast. Tijdelijke G-code blijft buiten de repository. Je kunt na een
wijziging ook enkele delen testen, bijvoorbeeld `cad/slice_check.py 01_romp_2`.
Bij een gerichte hercontrole worden eerdere resultaten alleen hergebruikt
als de overige 3MF-bestanden byte-identiek zijn en de opgeloste printer-,
proces- en filamentinstellingen exact overeenkomen. Ontbreken die tijdelijke
profielen, draai dan de volledige controle opnieuw. De eigen
profielbestanden staan in `../print/profielen/`.

## Constructie en coördinaten

- X = lengte, 0 achter / boeg aan dek 900 / top verschansing 910.
- Y = bakboord positief, Z = hoogte boven de kiel. De browservormstudie
  gebruikt Y omhoog en Z stuurboord; de CAD-viewer roteert de assen correct.
- Holle romp: 3 mm horizontale binnenoffset plus 3 mm verticale bodemoffset.
  Dit houdt schuine kimmen stevig, met lokaal meer dan 3 mm materiaal.
- Sneden: 227,5 / 455 / 682,5 mm; de laatste rompsectie is 217,5 mm lang.
- Lasstroken: 24 mm lang, 2,4 mm extra horizontale/verticale offset,
  nominale lijmspeling 0,25 mm in beide richtingen.
- Dekken: 3 mm; accommodatie: 1,6 mm. Alle georiënteerde printdelen ≤246 mm.
- Achterste serviceluik; voorste hoofddekpanelen vormen met lijmstrips één
  afneembare drager voor de bovenbouw, met optionele M3-borging.
- RC-platen zijn generiek. As-, roerkoker- en boegschroefgaten zijn nog dicht;
  werkelijke hardware bepaalt de uiteindelijke doorvoeren en bevestigingen.

Zie [`../print/BOUWHANDLEIDING.md`](../print/BOUWHANDLEIDING.md) voor printstand,
aantallen, montage, tolerantieproeven en fysieke vervolgcontroles.

API-referentie: [CadQuery import/export](https://cadquery.readthedocs.io/en/latest/importexport.html).
