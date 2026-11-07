# Build Labs

**[Open de startpagina met alle 3D-modellen →](index.html)**

Verzamelrepository voor Marks bouwprojecten. Elk project krijgt een eigen map
in de categorie waar het bij hoort, met een README die uitlegt wat het is en
hoe je ermee verder werkt.

## Inhoud

| Map | Wat erin staat |
|---|---|
| [`3d-models/`](3d-models/README.md) | 3D-ontwerpen: conceptmodellen in de browser, CAD-bronbestanden en printbestanden |

### 3D-modellen

| Project | Status | Beschrijving | Documentatie |
|---|---|---|---|
| [Ortelius RC](3d-models/ortelius/index.html) | Concept | RC-model van het poolexpeditieschip Ortelius, schaal 1:100, 91 cm | [README](3d-models/ortelius/README.md) |
| [Smit-Lloyd 109](3d-models/smit-lloyd-109/index.html) | Printbaar prototype (v17) | Afneembare bovenbouw voor een bestaande RC-romp, STEP en STL | [README](3d-models/smit-lloyd-109/README.md) |
| [Porsche 911 Targa 1971](3d-models/porsche-911-targa-1971/index.html) | Ontwerpfase | Referentiepagina met eigen foto’s, ontwerpkeuzes en vormchecklist | [README](3d-models/porsche-911-targa-1971/README.md) |
| [Dashboard: subwoofer](3d-models/porsche-911-f-model-dash-subwoofer/index.html) | Printklaar (v2.5.1) | Cup voor een Visaton W 100 X onder het dashboard van de 911 F-Model | [README](3d-models/porsche-911-f-model-dash-subwoofer/README.md) |
| [Dashboard: dubbele voorspeakers](3d-models/porsche-911-f-model-dash-double-front-speaker/index.html) | Ontwerp klaar (v7) | Adapterplaat voor twee Audison APX 4 in het dashboard van de 911 F-Model | [README](3d-models/porsche-911-f-model-dash-double-front-speaker/README.md) |

De projectnaam opent de projectpagina met het draaibare model of, zolang de
geometrie nog in ontwikkeling is, de referenties en ontwerpkeuzes.

## Online bekijken

Via GitHub Pages: **https://markmastop.github.io/buildlabs/index.html** — de startpagina
(`index.html` in de root) linkt naar alle modellen.

## Werken met de modellen

De conceptmodellen zijn losse HTML-pagina's met een draaibaar 3D-model
(three.js via CDN). Open `index.html` in een browser; een internetverbinding
is nodig voor de bibliotheek en de lettertypen.

## Printer

Ontwerpen zijn afgestemd op een **Bambu Lab P2S** (bouwvolume 256 × 256 × 256 mm)
met AMS. Grotere onderdelen worden in delen van maximaal ca. 225 mm opgedeeld.

## Wat gaat in Git?

Bronbestanden (CAD, HTML, documentatie), STL- en 3MF-printbestanden en
referentiefoto's met een duidelijke bron horen in de repository. Lokale
configuratie, slicer-tijdelijke bestanden, G-code en grote renders blijven
buiten Git; zie [`.gitignore`](.gitignore).
