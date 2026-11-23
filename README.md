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
| [Ortelius RC](3d-models/ortelius/index.html) | Printprototype p2 | 1:100 · 910 mm lang · STL · 3MF · STEP. RC-model van het poolexpeditieschip, met een vierdelige holle romp en afneembare vooropbouw. Print- en pasproefbestanden zijn beschikbaar. Fysieke passing, lekdichtheid en vaargedrag moeten nog worden getest. | [README](3d-models/ortelius/README.md) |
| [Smit-Lloyd 109 RC](3d-models/smit-lloyd-109/index.html) | Printprototype v18 | ca. 410 × 189 × 202 mm · STL · STEP. Afneembare bovenbouw voor een bestaande RC-romp, inclusief pasmal. De maat geldt voor de v18-bovenbouw. Fysieke passing op de romp moet nog worden getest. | [README](3d-models/smit-lloyd-109/README.md) |
| [Oasis of the Seas RC](3d-models/oasis-of-the-seas-rc/index.html) | Inbouwconcept | 1.000 mm lang · 5 rompsegmenten. RC-inbouwstudie met een romp van circa 133 mm breed midscheeps, twee schroefassen en gekoppelde roeren. Het project bevat kijkmodellen en een onderdelenlijst. | [README](3d-models/oasis-of-the-seas-rc/README.md) |
| [Porsche 911 Targa 1971 RC](3d-models/porsche-911-targa-1971/index.html) | Eerste printset | 1:10 · ca. 407 mm lang · STL · 3MF · STEP. Tweedelige carrosserie met interieur, ruiten en uitneembaar dak. Voor de RC-uitvoering is een Tamiya M-06M-chassis op 225 mm wielbasis nodig. De passing moet nog fysiek worden getest. Voor het vitrinemodel zijn asdragers en sierwielen meegeleverd. | [README](3d-models/porsche-911-targa-1971/README.md) |
| [Dashboard: subwoofer](3d-models/porsche-911-f-model-dash-subwoofer/index.html) | Final v2.5.1 | 160 × 118 × 70 mm · STL. Cup met montageplaat voor een Visaton W 100 X van 10 cm onder het dashboard. De passing in de auto moet nog worden getest. | [README](3d-models/porsche-911-f-model-dash-subwoofer/README.md) |
| [Dashboard: dubbele voorspeakers](3d-models/porsche-911-f-model-dash-double-front-speaker/index.html) | Final v7 | 230 × 106 × 12 mm · STL. Adapterplaat voor twee Audison APX 4 van 10 cm. De plaat is 9 mm dik en meet 12 mm met de middenrib. De passing in de auto moet nog worden getest. | [README](3d-models/porsche-911-f-model-dash-double-front-speaker/README.md) |
| [EnergyDeck 7-inch behuizing](3d-models/energydeck-7-inch/index.html) | Final v9 | Voet 126 × 120 mm · STL · STEP. Bureaustandaard met schuifframe voor het ELECROW CrowPanel Advance 7.0 (DIS02170A). De hoogte met voorframe is circa 232 mm. | [README](3d-models/energydeck-7-inch/README.md) |
| [EnergyDeck 5-inch behuizing](3d-models/energydeck-5-inch/index.html) | Final | Voet 108 × 80 mm · STL · STEP. Bureaustandaard voor het ELECROW CrowPanel Advance 5.0 ESP32-S3-touchdisplay, met de fabrieksplaten gemonteerd. Digitaal gecontroleerd en gesliced. Fysieke passing moet nog worden getest. | [README](3d-models/energydeck-5-inch/README.md) |
| [Zes geometrische workshopmodellen](3d-models/workshopmodellen/index.html) | Final | Max. 80 mm per model · 6 STL · Blender. Zes modellen voor workshops: een robot, sleutel, boogbrug, kompas, huis en boom met takken. | [README](3d-models/workshopmodellen/README.md) |
| [Truma Therme-montageplaat](3d-models/truma-therme-montageplaat/index.html) | Final v17 | 78 × 61 × 29 mm · STL. Montageplaat op schaal 1:1 voor de bediening van een Truma Therme, met een halfronde kabeluitsparing tegenover de knop. | [README](3d-models/truma-therme-montageplaat/README.md) |

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
