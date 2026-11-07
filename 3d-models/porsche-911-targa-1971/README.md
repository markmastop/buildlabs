# Porsche 911 Targa 1971

**[Open de projectpagina →](index.html)**

Decoratief 3D-printmodel van Marks eigen **Porsche 911 Targa uit 1971**.

**Status: eerste bewerkbare 3D-vormconcept v1; gelijkenis nog te beoordelen.**
Er is een nieuw 3D-vormconcept met afzonderlijke onderdelen. De vorm is nog niet goedgekeurd. Mark wees de eerste geometrie af
op gelijkenis. Op zijn verzoek is de mini met alle bijbehorende bestanden buiten
deze overdracht gelaten.

## Begin hier

1. Lees de [ontwerpbrief](ONTWERPBRIEF.md), inclusief de concrete vormkritiek.
2. Gebruik de [drie echte referentiefoto’s](referentie/README.md) voor de vorm.
3. Lees de [overdracht en bronkandidaten](OVERDRACHT.md) voordat je een basis kiest.

## Bevestigde gegevens en keuzes

- Auto: Porsche 911 Targa, bouwjaar 1971; door Mark bevestigd.
- Doel: decoratief schaalmodel, met een herkenbare vroege 911-carrosserie.
- Printer: Bambu Lab P2S **met AMS**.
- Eerste grotere voorstel: circa **20 cm** lang, met geel-oranje, zwart en zilvergrijs.
- Dit is een ontwerprichting. Een exacte schaal en definitieve maat zijn nog niet
  vastgesteld; de vorm van het 20 cm-concept is niet goedgekeurd.
- De nozzle van 0,4 mm en PLA zijn eerdere werkuitgangspunten, niet door Mark
  apart bevestigde instellingen. P2S-bouwvolume: 25,6 × 25,6 × 25,6 cm.

## Bestanden

| Map of bestand | Betekenis |
|---|---|
| [index.html](index.html) | Referentiepagina met fotowissel, kleurvoorstel en bewaarde vormchecklist |
| [ONTWERPBRIEF.md](ONTWERPBRIEF.md) | Vorm, gemaakte keuzes en criteria voor de volgende versie |
| [OVERDRACHT.md](OVERDRACHT.md) | Herkomst, bronkandidaten, beperkingen en vervolg |
| [referentie/](referentie/README.md) | Echte foto’s van voorzijde, achterzijde en interieur |
| [concept/](concept/README.md) | Historisch beeldvoorstel van 20 cm en generatieprompt; geen bijbehorende CAD |
| [overdrachtsbestanden.json](overdrachtsbestanden.json) | Herkomst, hashes en Git-status van gekopieerde bestanden |

De originele AI-visualisatie staat lokaal in `concept/renders/`; renders zijn
volgens de repo-afspraken uitgesloten van Git. De bronnen in het iCloud-project
zijn behouden; er zijn kopieën gemaakt. Er staan hier geen bestanden uit de afgewezen poging. De nieuwe Blender-bron staat in `cad/`.

## Volgende stap

Kies een correcte vroege 911-carrosserie als basis en werk de Targa-uitvoering
uit. Beoordeel zijaanzicht, vooraanzicht en beide driekwartaanzichten van de
werkelijke CAD-geometrie voordat dunne details worden aangepast voor het printen.
De technische printcontrole volgt op een herkenbare carrosserievorm.

De zelfstandige `index.html` bevat het 3D-kijkmodel als ingebedde GLB, three.js
0.160.1 via CDN, vaste aanzichten en de echte referentiefoto’s. Het model is ook
los beschikbaar als `model/911-targa-concept-v1.glb`. De bron staat in
`cad/911-targa-concept-v1.blend` en het reproduceerbare `cad/maak_concept.py`.

Blender-coördinaten zijn centimeters; de GLB-export gebruikt de standaard
glTF-eenheden. De viewer normaliseert de carrosserielengte naar 20 cm op
modelschaal. Dit is een ontwerpmaat, geen vastgestelde schaal of maatvaste scan.
De vorm is handmatig opgebouwd naar de drie eigen foto’s en het grotere
beeldvoorstel. Zie `cad/modelgegevens.json`. Er zijn geen merklogo’s toegevoegd.

Dit concept bestaat uit losse oppervlakken en overlappende onderdelen. Er is
nog geen controle op gesloten printvolumes, minimale diktes, passing of support.
Er worden daarom geen STL/3MF-printbestanden aangeboden. Beoordeel eerst de
herkenbaarheid vanuit de drie aanzichten en vergelijk met de foto’s.
