# Build Labs

Verzamelrepository voor Marks bouwprojecten. Elk project krijgt een eigen map
in de categorie waar het bij hoort, met een README die uitlegt wat het is en
hoe je ermee verder werkt.

## Inhoud

| Map | Wat erin staat |
|---|---|
| [`3d-models/`](3d-models/README.md) | 3D-ontwerpen: conceptmodellen in de browser, CAD-bronbestanden en printbestanden |

### 3D-modellen

| Project | Status | Beschrijving |
|---|---|---|
| [Ortelius RC](3d-models/ortelius/README.md) | Concept | RC-model van het poolexpeditieschip Ortelius, schaal 1:100, 91 cm |
| [Smit-Lloyd 109](3d-models/smit-lloyd-109/README.md) | Printbaar prototype (v17) | Afneembare bovenbouw voor een bestaande RC-romp, STEP en STL |

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
