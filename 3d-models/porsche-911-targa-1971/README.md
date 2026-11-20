# Porsche 911 Targa 1971

**[Open de projectpagina →](index.html)**

Decoratief 3D-printmodel van Marks eigen **Porsche 911 Targa uit 1971**.

**Status · Vierde carrosseriestudie op schaal 1:10, ter beoordeling.**
De eerste grotere 3D-uitwerking week volgens Mark te veel af van het voorstel en wordt niet op de projectpagina getoond. Mark wees de eerste geometrie af
op gelijkenis. Op zijn verzoek is de mini met alle bijbehorende bestanden buiten
deze overdracht gelaten.

## Begin hier

1. Lees de [ontwerpbrief](ONTWERPBRIEF.md), inclusief de concrete vormkritiek.
2. Gebruik de drie lokale referentiefoto’s in `images/porsche/` voor de vorm.
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

## RC-versie op het M-06M-chassis

De [projectpagina](index.html) toont de Targa, het losse chassis en de Targa op het chassis.
In de gecombineerde weergave staan de kitwielen onder de carrosserie. De twee
wielbasissen zijn rond hetzelfde midden uitgelijnd. De Targa heeft een wielbasis
van 226,8 mm, waardoor de kitassen aan beide uiteinden 0,9 mm verder naar binnen liggen.
De ashoogte bepaalt de voorlopige montagehoogte.

De chassislaag gebruikt centimeters op modelschaal. De wielbasis is 22,5 cm,
de spoorbreedte voor en achter 13,8 cm en de banden zijn 5,9 cm in diameter en
2,5 cm breed. Deze maten komen uit de [Tamiya-specificatie voor kit 58572](https://www.tamiya.com/japan/products/58572/index.html).
De vorm en plaats van frame, accu, ophanging, achterste motorunit en montagepennen
zijn benaderd aan de hand van de foto's in `images/chasis/`. De fysieke montagehoogte,
penposities en vrije ruimte bij insturen en inveren moeten aan de gebouwde kit worden gemeten.

- **Schaal:** 1/10. Lengte circa 416 mm, wielbasis circa 227 mm. Een grote
  schaal is bewust gekozen; kleiner hoeft niet.
- **Chassis:** Tamiya M-06 (achterwielaandrijving, motor achterin, zoals de 911).
  Mark koopt de Volkswagen Beetle-kit (58572, circa €110,83). Wielbasis
  variabel: 210, 225 of 239 mm. **Instelling: 225 mm**, circa 2 mm onder de
  227 mm op 1/10. De kit bevat motor (540), regelaar (TEU-105BK), banden en
  velgen en een Kever-body, die niet wordt gebruikt.
- **Elektronica:** Mark heeft een FlySky ST8-zender. Nog te kopen: servo,
  ontvanger, accu en lader. Zie de [RC-bestellijst](RC-BESTELLIJST.md). De
  regelaar van de kit werkt volgens Tamiya op 6,6–7,2 V: kies 6-cels NiMH.
- **Body:** wordt los van het chassis ontworpen voor de M-06. Op 1/10 is
  de body langer dan het bouwvolume van de P2S (256 mm), dus verdeel hem in
  twee of drie delen met pasranden of lijmvlakken.
- **Sterkte:** het open Targadak maakt de body minder stijf. Gebruik dikkere
  wanden (circa 1,2–1,6 mm), een versterkte beugel en dakrand en eventueel een
  interieurplaat.
- **Later:** een eigen geprint chassis is mogelijk, maar vraagt PETG of nylon,
  proefprints en een eigen geometrie. Eerst rijden op de M-06.
- **Nog vast te stellen:** werkelijke wielbasis en spoorbreedte van de 1971
  Targa, bodymontage (bodyclips), ruimte rond de wielkasten en de verdeling in
  delen. Prijzen en voorraad zijn niet vastgelegd.

## Bestanden

| Map of bestand | Betekenis |
|---|---|
| [index.html](index.html) | Het Targa-voorstel, de 3D-viewer met afzonderlijke chassislaag en de vormchecklist |
| [ONTWERPBRIEF.md](ONTWERPBRIEF.md) | Vorm, gemaakte keuzes en criteria voor de volgende versie |
| [bestellen.html](bestellen.html) en [RC-BESTELLIJST.md](RC-BESTELLIJST.md) | Bestellijst met winkellinks en checklist voor de RC-versie op Tamiya M-06 |
| [OVERDRACHT.md](OVERDRACHT.md) | Herkomst, bronkandidaten, beperkingen en vervolg |
| `images/porsche/` | Lokale foto’s van de eigen auto en het interieur |
| `images/chasis/` | Lokale referentiebeelden van het Tamiya M-06-chassis |
| [concept/](concept/README.md) | Historisch beeldvoorstel van 20 cm en generatieprompt; geen bijbehorende CAD |
| [overdrachtsbestanden.json](overdrachtsbestanden.json) | Herkomst, hashes en Git-status van gekopieerde bestanden |

De originele AI-visualisatie staat lokaal in `concept/renders/`. Een bytegelijke
weergavekopie staat in `concept/ontwerpvoorstel.png` en is opgenomen in Git, zodat
het beeld op de projectpagina beschikbaar is. De bronnen in het iCloud-project
zijn behouden; er zijn kopieën gemaakt. Er staan hier geen bestanden uit de afgewezen poging. De nieuwe Blender-bron staat in `cad/`.

## Volgende stap

Vergelijk het zijprofiel en beide driekwartaanzichten in de viewer met de foto’s
van de vroege 911 en Marks eigen Targa. Gebruik die vergelijking om de vorm te
beoordelen voordat de carrosserie voor het printen wordt uitgewerkt.
De technische printcontrole volgt op een herkenbare carrosserievorm.

De zelfstandige `index.html` toont het oorspronkelijke grotere Targa-voorstel
en de interactieve vormstudie. Het voorstel is een AI-visualisatie, geen
CAD-render of bewijs van printbaarheid. Het grote beeld is ook los te openen.

De afgewezen grotere 3D-uitwerking is alleen als historie bewaard in `cad/` en
`model/`; zij wordt niet meer in de pagina geladen en niet aangeboden als
passend model. De afgewezen mini is niet opgenomen. Voor toekomstige
browsergeometrie gelden centimeters op modelschaal en voor printbestanden
millimeters. De vierde carrosseriestudie volgt het open zijprofiel van de rode
Targa op de aangeleverde foto. De voorste spatborden lopen geleidelijk op en de
achterruit loopt vrijwel recht af naar de motorklep. **Zijkant** toont de auto
met de neus naar links en weinig perspectief, zoals op de foto.
De knop **Staart** toont de auto recht van achteren met een kleine beeldhoek.
**Achter** toont de achterzijde schuin vanaf de bestuurderskant, zoals op de
foto van Marks auto. Het digitale model met open dak meet circa
40,5 × 16,4 × 12,9 cm inclusief spiegel en bumperhoorns. Gelijkenis en
fysieke passing op het chassis moeten nog worden beoordeeld.
