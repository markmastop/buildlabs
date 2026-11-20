# Ontwerpbrief: een herkenbare 911 Targa

## Auto en referentie

Het vaste uitgangspunt is Marks Porsche 911 Targa uit 1971. Het model en bouwjaar
zijn bevestigd; vraag die niet opnieuw. De foto’s zijn de vormreferentie. Ze tonen
een geel-oranje carrosserie, vroege smalle bumpers met chroomaccenten, vijfbladige
velgen, een zilverkleurige Targaband, een grote gebogen achterruit en een zwart
interieur met pepita-bekleding. “Bahamageel” kwam in de chat uit het dealerbord;
de exacte lakcode is niet vastgesteld.

## Gewenst resultaat

Een decoratief, vereenvoudigd model dat direct als vroege 911 Targa herkenbaar is.
Mark koos een decoratief model voor zijn Bambu P2S en bevestigde een AMS.
Het grotere voorstel was circa 20 × 8 × 6–6,5 cm, met drie kleuren: geel-oranje,
zwart en zilvergrijs. Dat voorstel is alleen een AI-beeld; er bestaat geen
overeenkomstig CAD-model en geen expliciete goedkeuring van de vorm.

De maten zijn ontwerpmaten, geen vastgelegde schaal. Open dak, vaste wielen,
massieve donkere raaminzetten en een losse sokkel waren voorstellen van de
assistent, geen afzonderlijk goedgekeurde eindkeuzes. De sokkel was circa
22,5 × 10,5 × 0,8 cm. In het AI-beeld is de maatlijn illustratief: 20 cm sloeg op
de auto, niet op de sokkel.

## Vormkritiek uit de afgewezen poging

De bestanden van die poging zijn op verzoek niet overgenomen. De belangrijkste
lessen voor een nieuw ontwerp zijn:

- Koplampen moeten schuin in hoge, afgeronde en doorlopende spatbordtoppen
  liggen. Losse bolletjes op de motorkap geven de verkeerde vorm.
- Behoud de lange lage voorklep tussen de spatborden en de afgeronde voorhoeken.
  Een brede vlakke voorkant mist het 911-profiel.
- Maak de ronde wielschouders, taille en onderdorpel zichtbaar. Een hoge rechte
  zijwand tot aan de grond maakt van de carrosserie een massieve bak.
- De voorruit en het raamkader lopen taps toe en zijn gebogen; geen losse
  rechthoekige plaat.
- De Targa heeft een brede omvattende band met een grote bolle achterruit.
  Een smalle balk op twee rechte paaltjes is onvoldoende herkenbaar.
- Behoud de ronde achterste schouders en de vloeiende overgang van beugel via
  achterruit naar de aflopende motorklep en afgeronde staart.

Geslaagde mesh- en slicecontroles bewijzen technische geometrie, niet gelijkenis.

## Werkwijze voor het herontwerp

1. Begin met een passende vroege 911-bronmesh of met betrouwbare zij-, boven- en
   voorprofielen en meerdere gemeten dwarsdoorsneden. Gebruik de eigen foto’s
   om de details van deze Targa te vergelijken.
2. Controleer bij een bronmesh de generatie en carrosserievorm. Een vroege coupé
   is hoogstens een basis; het Targadak en de achterruit moeten dan echt worden
   aangepast. Controleer de actuele gebruiksvoorwaarden vóór verwerking.
3. Maak beelden van dezelfde geometrie die later wordt geëxporteerd: zijaanzicht,
   voorzijde, voor-driekwart en achter-driekwart. Een nieuw AI-plaatje is geen
   bewijs dat het 3D-bestand klopt.
4. Behoud de herkenbare proporties wanneer details dikker of eenvoudiger moeten
   worden. Werk pas daarna de onderdelen en printoriëntatie uit.
5. Controleer gesloten volumes, losse delen, minimumdiktes, passing en de slice.
   Een fysieke proefprint blijft nodig om de werkelijke print te beoordelen.

## Eerste 3D-vormstudie (november 2026)

Op de projectpagina staat een parametrische vormstudie in three.js (r128,
vastgepind), schaal 1:10, in `index.html`. Mark vond de gelijkenis van deze eerste
vormstudie met zijn Targa over de hele carrosserie te gering.

- Maten (ware grootte): het profiel (hoogtes, neus, dorpel, wielkasten, Targabeugel,
  achterruit en staart) is uitgemeten aan een zijfoto van een vroege 911 Targa en
  geschaald op de wielbasis van 2268 mm. Zo komt de lengte op circa 4010 mm en de
  hoogte op circa 1260 mm, tegen de gangbare opgave 4163 en 1320 mm. Breedte
  1610 mm en wielstraal 322 mm. Op 1:10: circa 40,1 × 16,1 × 12,6 cm.
- De carrosserie is een dwarsdoorsnede-loft: per station (circa elke 25 mm)
  bepalen breedte, bovenrand, motorkap- of dakhoogte en wielkasten de vorm.
  Ruiten, Targabeugel, rooster, lampen, bumpers en wielen zijn losse onderdelen.
- Alle doorsneden en hoogtes zijn **schattingen** uit de eigen foto's en
  gangbare 911-hoofdmaten, geen scan en geen exacte reconstructie.
- Bewuste vereenvoudigingen: de motorkap en deuren zijn geen aparte delen,
  het interieur is een eenvoudige indicatie, merkplaatjes ontbreken.
- Zwakke punten om te beoordelen: de vorm van de neus en de koplampen, de
  staart en achterschouders, het kozijn en de bolle achterruit.

## Tweede carrosseriestudie (november 2026)

De geometrie op de projectpagina is opnieuw uitgewerkt met de lokale foto's in
`images/porsche/`. Op de zijfoto `images-12.jpg` bepalen de twee wielcentra de
schaal voor de vergelijking. De dorpels zijn verlaagd. De deur heeft een gebogen
onderrand en loopt achter schuin op naar de voet van de beugel. De kruin van
het dak is verlaagd en beide ruitkaders sluiten daarop aan.

De frontfoto `images-14.jpg` en Marks eigen voor-driekwartfoto geven de hoge
lampkruinen en de lage, licht bolle voorklep aan. De lampopeningen zijn in de
spatbordhuid gevormd. De detailfoto `images-6.jpg`, het achteraanzicht
`images-13.jpg` en Marks achter-driekwartfoto geven de breedte van de
Targabeugel, de gebogen onderrand van de achterruit en het verloop van de
schouders naar de achterlichten aan.

De volledige digitale auto meet met open dak circa 40,7 × 16,3 × 12,5 cm.
De wielbasis van de vormstudie is 22,68 cm en die van het M-06M-chassis is
22,5 cm. De referentieauto's verschillen in uitrusting en de foto's hebben
perspectief. Dwarsdoorsneden, ruitbolling en uiteindelijke passing blijven
schattingen tot ze met de auto en het chassis zijn vergeleken.

## RC-versie

Mark wil ook een bestuurbare uitvoering. Uitgangspunten, na goedkeuring van de
vorm:

- Schaal 1/10 op een Tamiya M-06 (Volkswagen Beetle-kit, 58572), 2WD
  achterwielaandrijving met motor achterin. Wielbasis instellen op **225 mm**;
  de 911 F-modellen hebben circa 2268 mm, dus circa 227 mm op 1/10. Controleer
  de wielbasis van de 1971 Targa.
- De body wordt los van het chassis ontworpen. Hij is circa 416 mm lang en past
  niet in één keer op de P2S (256 mm): verdeel hem met pasranden of lijmvlakken.
- Houd rekening met het open dak: dikkere wanden, versterkte beugel en dakrand
  en eventueel een interieurplaat. Bodymontage met bodyclips; maak ruimte voor
  wielkasten en bandenspel.
- Zender: FlySky ST8 (van Mark). Servo, ontvanger, accu en lader nog te kopen.
- Een eigen chassis kan later; eerst rijden op de M-06.

## Printuitgangspunten

De nozzle van 0,4 mm en PLA zijn eerdere aannames die bij de uitwerking moeten
worden gecontroleerd. Eerdere ontwerpdoelen waren 1,6–2 mm voor wanden en 2–3 mm
voor vrijstaande beugel/ruitranden; dit zijn geen universele printerminima.

Kleurverdeling via de AMS: geel-oranje carrosserie, zwart voor banden/interieur/
ramen en zilvergrijs voor beugel, velgdetails en accenten. Onderdelen kunnen los
blijven waar dat de printoriëntatie of het aantal kleurwissels verbetert.
Voor het nieuwe model zijn printtijd, materiaalverbruik, passing en ondersteuning
nog niet vastgesteld. Er is geen fysieke proefprint van een goedgekeurd model.
