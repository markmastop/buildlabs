# Ontwerp Ortelius RC — vormstudie v3

De vormstudie v3 is de visuele bron van het constructieprototype p1.
De CAD-bron en STEP staan in `cad/`, de STL/3MF en controles in `print/`.
Zie [CAD-weergave](cad/index.html) en [bouwbeschrijving](print/BOUWHANDLEIDING.md).
De onderstaande fotocontrole beschrijft de oorspronkelijke browserstudie.
Alle geometrie staat zelfstandig in [`index.html`](index.html), met Three.js
r128 via vastgepinde CDN-links. Er is geen buildstap.

## Maten en herkomst

Maten zijn in **centimeters op modelschaal 1:100**: 1 cm model = 1 m echt.
De gekozen lengte over alles is circa 91 cm: de gesloten voorromp eindigt
op x = 90 en de uitwaaierende witte verschansing reikt tot circa x = 91.
De maximale rompbreedte is 17,2 cm en de getekende waterlijn ligt 5,4 cm
boven de kiel. Uitrusting en veiligheidsnetten steken buiten de rompbreedte.
De lengte is een modeluitgangspunt, geen opgemeten scheepsbouwkundige maat.

Bronnen van de gekozen hoofdmaten:

- [Oceanwide, kenmerken Ortelius](https://oceanwide-expeditions.com/blog/15-features-figures-and-facts-about-ortelius)
- [MV Ortelius](https://en.wikipedia.org/wiki/MV_Ortelius)
- [Oceanwide, plaats van het helidek](https://oceanwide-expeditions.com/faq/where-is-the-helicopter-deck-located)

Deze bronnen waren al onderdeel van het project. In deze wijziging zijn de
bestaande hoofdmaten aangehouden; er is geen scheepsbouwkundig lijnenplan
beschikbaar. Dekhoogtes, ramen, posities van uitrusting en onderwatervorm
zijn **schattingen uit foto's**, geen opgemeten of goedgekeurde bouwmaten.
Het eerder genoemde vaargewicht van circa 4 kg blijft een doel, geen uit dit
browsermodel berekende waterverplaatsing of stabiliteitscontrole.

## Fotocontrole en wijzigingen

De 34 beeldbestanden staan lokaal in `images/`: 33 genummerde JPG's en
`MV_Ortelius_In_Terra_Nova_Bay.png`. Foto 30 is het bruikbaarste bijna haakse
zijaanzicht; 32/33 tonen het achterschip, 22–26 de dekdetails. Sommige
bestanden tonen dezelfde opname in een andere versie (zie het referentieoverzicht).
Ze zijn buiten Git gehouden; het browsermodel laadt ze niet. De foto's tonen
verschillende kleurstellingen en uitrusting. De geometrie hieronder is een
vormstudie op basis van die verzameling, geen vastgelegde historische toestand.

| Referentie | Zichtbare kenmerken | Aanpassing in v2 |
|---|---|---|
| 02, 06, 08, 09 | Zijprofiel, dekniveaus, schoorsteen en sloepen | Posities herverdeeld; lage accommodatie met kleinere patrijspoorten, smaller hoger dekhuis en open gangboorden |
| 13, 18, 19 + zijfoto 07-11 | Brug, dekhoogtes en positie voorste opbouw | Precies drie witte lagen boven de romp (dek 1, dek 2, brug, elk ~3 cm); de hele voorste opbouw ~5 cm naar achteren. De brug is recht en bijna even breed als het schip, met één rij van 11 frontramen. Erachter staat een smaller dekhuis met het naambord op het kompasdek en een schuine mantel achter de radarmast. Gecontroleerd met een overlay op de zijfoto |
| Zijfoto 07-11 (ronde 5) | Achterschip, schoorsteen en voorsteven | Schoorsteen 4,5 cm naar achteren met een naar achteren oplopende kap, de mast tegen het front en drie uitlaten op een rij. Hangar loopt van 17,5 tot 36,5 en is 3,9 cm hoog. Helidek ingekort tot 0–17,5. Dek 1 loopt door tot de hangar en dek 2 eindigt met een rechte achterwand op x 41,4. Sloepen en davits 1,8 lager. Voorsteven sterker hellend (waterlijn x 84,6, dek x 90); witte, bijna vlakke verschansing met verhaalgaten tot de punt op x 91; ankerkuil lager in de boeg |
| Zijfoto 07-11 (ronde 6) | Bakverschansing, achterschip en valreep | Verschansing voor is nu één doorlopende wand precies op de dekrand die naar de punt toe naar buiten uitwaaiert, zonder losse blokken of naden. Achterschip: blauwe romp tot 11,9 met daarboven open poorten tot het dek en een teruggezette witte wand met ramen; de dekrand is blauw. Valreep aan bakboord uitgezet (x 13,8 → 19,9) met bordes en rode boei, aan stuurboord gestuwd. Boegschroefmerken met kruis voor en achter. Trap van het sloependek naar het hangardak teruggezet |
| Luchtfoto 07-11 (klein) | Dekkleuren van boven | Kompasdek groen in plaats van grijs, zoals de overige dekken; verder bevestigt de foto de indeling van de bak, de brug met de radarmast achteraan en de sloepen |
| 32, 33 (achteraanzichten) | Hangar, helidek en promenadedek | Hangar bijna scheepsbreed tot x 29,8 met een grote deuropening (12,4 breed, afgeschuinde bovenhoeken). Hangardak zonder blauwe dekzeilen: een witte kast en de windzakmast in het midden. Dichte witte verschansing rond het promenadedek onder het helidek, met een grote witte tank dwarsscheeps tegen de spiegel. Scheepsnaam alleen nog op de spiegel, niet op de zijkant |
| 03, 07, 11, 15 | Getrapte spiegel en open achterdekken | Lagere achterromp en twee open niveaus met kolommen en witte randliggers |
| 05, 14 | Helidek, hangaringang en veiligheidsnetten | Groter, afgeschuind helidek met open netstructuur en zichtbare hangaringang |
| 06, 09, 14 | Schoorsteenkap, uitlaten, mast en davits | Schuine witte mantel, oplopende zwarte kap, drie mastarmen en geknikte sloepdavits |
| 07, 16 | Droogdok en boeg | Oplopend onderwaterschip achter en smallere kiel; verdere onderwatervorm blijft onzeker |

De scheepsnaam is behouden. Het gekleurde embleem op de schoorsteen is
verwijderd; het model heeft geen rederijlogo's. De valreep hangt aan bakboord uitgezet
boven het water (zoals op de zijfoto); aan stuurboord ligt hij gestuwd tegen de romp.

## Aanpassingen in v3 na de nieuwe analyse

De lengteposities van brugfront (x 69,6), witte radarmast (58,9), zwarte mast
(33,3), sloepen (34,6) en hangaringang (17,5) zijn aangehouden. Er is geen
nieuwe algemene hoogte- of lengtecorrectie op het zijraster gebaseerd:
foto en model hebben niet automatisch dezelfde camerahoek of verticale schaal.

- **Open middenschip:** drie echte trapeziumvormige openingen per zijde,
  tussen x 41,4 en 61,2. De stijlen staan schuin. Een smaller binnenhuis
  laat zichtbare diepte en een gangboord achter de buitenwand vrij.
- **Ramen:** de ronde punten in de witte accommodatie zijn vervangen door
  smalle ramen met afgeronde hoeken, in paren en enkele losse groepen.
  Bakboord en stuurboord hebben afzonderlijke plaatsingslijsten. Het exacte
  aantal en de plaatsing blijven fotogebaseerde schattingen.
- **Hangar:** de twee volle blokken achter het donkere deurvlak zijn vervangen
  door vloer, zijwanden, een achterwand en een voorwand met een echte opening.
  De opening is 12,4 cm breed onderaan, met afgeschuinde bovenhoeken.
  De zichtbare binnendiepte is circa 12 cm. Spanten, kasten en een eenvoudige
  werkbok zijn ter ondersteuning van het beeld toegevoegd; hun maten zijn
  niet gemeten. De reddingsboten staan buiten de hangar op losse zijplatforms.
- **Dekdetails:** glazen lichtkap en houten banken achter de witte mast naar
  foto's 24–26. De zodiacs liggen in de achterste galerijen; reddingsvlotten
  zijn naar het lagere gangboord verplaatst. De knikarmkranen zijn compacter.
- **Achterdekken:** rechthoekige kolommen, dwarsliggers, korte schoren en
  raamopeningen met terugliggende ruiten in de onderste accommodatie.
- **Sloepen/davits:** cabine met vlakke facetten, smallere stootrand,
  dubbele geknikte armen met dwarsverbindingen en hydraulische cilinders.
- **Bekijken:** detailstanden **Middenschip** en **Hangar** naast de zes
  bestaande overzichtsaanzichten; de modelpagina blijft één zelfstandig HTML-bestand.

De invulling achter de galerijen, stuwage en kleinere uitrusting is een
visuele reconstructie. Een foto'set uit verschillende toestanden levert
nog geen exact gedateerde uitvoering of bouwtekening op. In die vormstudieronde is alleen het
browsermodel aangepast. De latere CAD-uitwerking p1 staat onderaan dit document.

## Assen en belangrijkste stations

- **x:** lengte, achtersteven = 0, boeg aan dek = 91.
- **y:** hoogte, kiel = 0, waterlijn = 5,4.
- **z:** breedte, middenlijn = 0; +z = stuurboord, −z = bakboord.

| Deel | x-bereik | Hoogte y | Breedte / keuze |
|---|---|---|---|
| Achterste werkvloer | 0,2–24,2 | 10,7 | Max. 16,6; afgeschuinde hoeken |
| Promenadedek achter | 0,2–24,2 | 13,9 | Max. 17,4; open ruimte eronder |
| Hoofddek voor | 24–90 | 13,9 | Volgt de rompvorm; witte verschansing tot x 91 |
| Lage accommodatie (dek 1) | 17,5–71,4 | 13,9–16,6 | Max. 16,4 |
| Open galerijen (dek 2) | 41,4–61,2 | 16,6–19,3 | Buitenwanden op z ±7,8; drie openingen per zijde |
| Binnenhuis achter galerijen | 42–60,8 | 16,6–19,3 | Breedte 9,3; teruggezet achter de buitenwanden |
| Hoger voorhuis (dek 2) | 60,5–69,8 | 16,6–19,3 | Breedte ca. 13,2–13,6; gefacetteerd front |
| Brug | 64,1–69,6 stuurhuis, 58,5–64,3 dekhuis | 19,3–22,3 | Recht front, stuurhuis max. 16,0 breed, dekhuis 12,0 |
| Kompasdek | 58,3–69,9 | 22,6 | Max. 16,5 voor, 12,4 achter; naambord ORTELIUS aan beide zijden |
| Hangar | 17,5–29,8 breed / tot 36,5 smal | 16,6–20,5 | Max. 16,0, rond de schoorsteen 11,8; deur 12,4 breed naar het helidek |
| Helidek | 0–17,5 | 16,75 | Max. 17,8 zonder netten |
| Schoorsteen | ca. 25,0–34,4 | 20,7–26,0 | Kap loopt naar achteren op, drie uitlaten |
| Sloepen | middelpunt 34,6 | onderzijde 17,65 | Twee gesloten sloepen met geknikte davits |
| Zodiacs / knikarmkranen | ca. 45,9 / 55,2 | stuwage op 16,6 / kranen op 19,3 | In de galerijen / compacte knikarmkranen |
| Glazen lichtkap | 49,2–55,0 | vanaf 19,41 | Breedte 6,0; schuin glas en banken ernaast |
| Zwarte mast | 33,3 | top 37,4 | Vakwerk met drie ra's, tegen het schoorsteenfront |
| Witte radarmast | 58,9 | top 36,2 | Twee draaiende radars, schuine mantel tot dek 2 |
| Voormast | 80,6 | top 27,2 | Slanker en lager dan de radarmast |

## Rompvorm

`hullStations` bevat per hoogte de halve breedte en de achterste/voorste x.
`station`, `hullHW`, `hullX0`, `bowX` en `hwAt` interpoleren deze doorsnedes.
De onderste gesloten romp loopt tot de achterste werkvloer op y = 10,7;
de blauwe verschansing reikt daar tot circa 11,9.
Daarboven begint de gesloten voorromp pas bij x = 24; zo blijven achter de
bovenliggende dekken twee echte open niveaus zichtbaar.

De kiel is versmald ten opzichte van v1 en de onderkant loopt naar achteren
op. Dit is nog geen definitieve keuze voor spanten, schroefraam, stevenbuis,
roerkoker of boegschroef. De getekende aandrijving is alleen een visuele indicatie.

## Bediening en vormcontrole

Vaste aanzichten: **Driekwart, Stuurboord, Bakboord, Boeg, Achterschip,
Bovenaanzicht**; detailstanden **Middenschip** en **Hangar**. Slepen en zoomen blijven beschikbaar. Het model begint stil,
zodat de vorm direct kan worden bekeken.

- **Water:** aan = waterlijn zichtbaar, onderwaterschip afgedekt; uit = hele romp.
- **Voorgestelde deelvlakken:** alleen rode hulplijnen, geen losse CAD-delen.
- **Bovenbouw eraf:** visuele animatie van de opbouw, geen uitgewerkte passing.
- **Avond:** licht uit de ramen; **Langzaam draaien:** automatische rotatie.

Beoordeel zijprofielen en brugfront, achterschip en bovenaanzicht. De pagina
linkt nu ook naar het aparte CAD-prototype en de printinstructies.

## Vervolg: printbare RC-constructie

Het printprototype p1 is nu uitgewerkt. Vier holle rompdelen zijn gesneden
bij x = 227,5 / 455 / 682,5 mm. De laatste sectie is 217,5 mm lang; de
uitwaaierende verschansing reikt als los deel tot x = 910 mm. Lasstroken,
opleglip, serviceluik, losse dekdrager en RC-platen staan in de CAD-bron.

Dit zijn modelbouwkundige constructiekeuzes. Gewicht, trim, hechting,
waterdichtheid, geselecteerde RC-producten en de fysieke passing moeten nog
met proefprints en hardware worden bevestigd.

## Werken in de bron

- `loft`: doorlopende, afgeronde rompdoorsnedes en sloepen.
- `tier`, `plan`, `slab`: hoekige dekken en corresponderende gevelvlakken.
- `sidePanel`: zijwangen en schoorsteenkap uit profielpolygonen.
- `panelGeometry`, `piercedSide`: wanden met echte openingen en dagkanten.
- `roundedOutline`, `windowPane`, `cabinGroups`: afgeronde ramen en plaatsing.
- `bench`: banken met houten planken en metalen onderstel.
- `galleryOpenings`, `hangar-interieur`, `lichtkap`: de nieuwe vormdelen van v3.
- `wallStrip`: doorlopende verschansing langs een polylijn, met uitwaaiering aan de bovenrand.
- `bridgeRing`, `bridgeAft`, `facadeWindows`: brug en glasvakken. De brug-groep `bg` gebruikt lokale x; `BDX` (−5) en `BL` verschuiven haar naar de wereldpositie.
- `Rods`, `railing`, `stairs`: masten, kolommen, relingen, davits en trappen.
- `viewDirections`, `positionView`: vaste camera-aanzichten.

De kleuren staan bij `NAVY`, `BOTTOM`, `WHITE`, `GLASS`, `GREEN`.

## Visueel RC-inbouwvoorstel

De knop **RC-inbouw** verbergt de buitengeometrie en toont de techniek met
een transparante referentie van de romp en dek-/waterlijncontouren. De
zichtbaarheid van buitenonderdelen en het water wordt bij terugschakelen
hersteld. **Labels** kan apart uit; de uitklapbare tabel bij de viewer bevat
alle ruimtematen. De bestaande vormstudie en fotogebaseerde hoofdposities
blijven behouden. De CAD- en printbestanden zijn apart uitgewerkt in p1.

| Onderdeel | Positie x (cm) | Keuze |
|---|---|---|
| Stevenbuis / koppeling | 3,5–23,5 / 23,5–25 | Loopt van y 2,2 naar y 4,1; motor ligt op dezelfde aslijn |
| Motor | 25–35 | Reserve Ø 6 × 10; schuine aslijn, neutrale mantel |
| Roerservo | 11 | Reserve 4,2 × 2 × 4; naast de as, met roerkoker/hefboom en stang |
| Accu 2S | 39–53 | Reserve 14 × 4,8 × 2,8; bak 16 × 6, laag op y 1,25 |
| Regelaars | 37 / 67 | Behuizingen 3,65 × 3,2 × 1,8; extra stekkerruimte niet meegerekend |
| Ontvanger | 55,5 | Reserve 5,5 × 3 × 2; op verhoogde montageplaat |
| Boegschroef | 76 | Open dwarstunnel ID 2, OD 2,3; generiek motorvolume Ø 2,4 × 3 |
| Ballastbakken | 57 / 63 | Twee lage bakken; gewicht nog te bepalen |

Alle maten behalve de regelaarbehuizing zijn voorlopige reserveringen. De
onderdelenlijst is geen bevestigde bestel- of compatibiliteitslijst. De
montageplaten zijn conceptueel; bevestigingen, schotten, doorvoeren, bereikbaarheid,
stabiliteit en werkelijk gekozen producten moeten bij CAD/inbouw nog worden
gecontroleerd. De bedrading is geen elektrisch schema.

Bron van de regelaarmaat: [Hobbywing-handleiding](https://www.hobbywing.com/en/uploads/file/20240315/4806bbdbab8eb9fea0bb26da87d81b00.pdf).
De bestaande productnamen krijgen in het model geen logo of merkopschrift.

## Gele helikopters en hangarpassing

De twee helikopters zijn neutrale fotogebaseerde AS350/H125-vormstudies op
1:100, geen exact geïdentificeerde of gecertificeerde vliegtuigmodellen.
De [Airbus-maattekening](https://www.airbus.com/sites/g/files/jlcbta136/files/2025-01/master-ground-rescue-booklet-h125.pdf)
geeft romplengte 10,93 m, rompbreedte 2,17 m, stabilisatorbreedte 2,53 m en
rotordiameter 10,69 m; dezelfde getallen zijn centimeters in het model.
De modelhoogte tot de rotornaaf is 3,14 cm. Uitvoering en kleurdetails zijn
vereenvoudigd en zonder registraties of logo's.

In de stallingsstand liggen de hoofdrotorbladen los in twee rekken langs de
hangarwanden. Er is geen fictief vouwmechanisme gemodelleerd.
[Oceanwide beschrijft bladverwijdering vóór stalling](https://oceanwide-expeditions.com/trip-log/otl22-24-trip-log-weddell-sea-in-search-of-the-emperor-penguin-incl-helicopters).

Beide helikopters hebben dezelfde maat: oorsprong x 21,3; z −3,2 / +3,2;
landingsvlak y = 16,81. Zonder hoofdrotorbladen beslaan ze ongeveer x 17,965
tot 28,895, y 16,81 tot 19,95 en z −4,465 tot −1,935 / +1,935 tot +4,465.
De opening is op deze plaatsen vrij tot y 20,15; de modelmarge erboven is
dus circa 0,20 cm (2 mm). De achterwand begint bij x 29,535. De modellen
kruisen elkaar en de bestaande hangarinrichting niet volgens de uitgevoerde
begrenzingsboxcontrole. Dit controleert statische modelruimte, geen echte
hangarmaten, rij-/draaibeweging of printtoleranties.

In de buitenstand staat één toestel met rotorbladen op het helidek en is
het andere op enige afstand in de lucht geplaatst, naar de referentiefoto.
De knoppen **Helikopter** en **Heli’s in hangar** geven detailweergaven.
De functie `helicopter()` maakt beide identieke modellen;
`positionHelicopters()` wisselt tussen buiten- en stallingsstand.


## CAD- en printprototype p1

Bronnen: [`cad/build.py`](cad/build.py), [`cad/parameters.json`](cad/parameters.json).
De STEP-assemblage en zelfstandige [CAD-viewer](cad/index.html) tonen dezelfde
geometrie als de printonderdelen. De units veranderen van cm in de browser
naar mm in CAD/print; CAD-assen X naar de boeg, Y bakboord, Z omhoog.

- 68 unieke delen, 146 exemplaren volgens de printlijst (inclusief 24 relingstroken,
  16 montageblokken, 8 deklijmstrips en proefstukken).
- Holle romp met 3 mm horizontale en 3 mm verticale binnenoffset; lokaal dikker
  voor stevige schuine kimmen. Vier secties en drie losse lasstroken.
- Nominale lijmspeling 0,25 mm horizontaal en verticaal; 24 mm overlapstrip,
  12 mm per zijde. Geen gegarandeerde printertolerantie zonder proef.
- Voorste dekken op een integrale lip, als gezamenlijke opbouwunit afneembaar.
  Achterste dek met afgedicht M3-serviceluik boven servo/as; losse borgblokken.
- Bovenbouw hol met echte raamgaten en open galerijen; hangardak afzonderlijk.
- Helikopterrompen in vlak printbare helften, met aparte skids en losse rotors.
- Maximaal printdeel 240 mm; alle delen blijven binnen 246 mm per as.
- De geschatte romp verplaatst bij 44 / 54 / 64 mm diepgang circa
  3,40 / 4,62 / 5,90 kg zoet water. Dit vervangt het onbevestigde modeldoel
  van circa 4 kg niet door een gegarandeerd vaargewicht.

Bewuste FDM-keuzes: vlakke versterkte vakwerkmast met losse ra’s, verdikte
staanders, solide lichtkap en sloepen, geschilderde ramen/markeringen en
losse generieke relingstroken. Veiligheidsnetten, touwen, kleine antennes,
zodiacs en ankerkettingen zijn modelbouwafwerking, geen losse p1-printdelen.
De accubak en montageplaten zijn adapters; de functionele doorvoeren blijven
dicht tot de echte as, roerkoker en boegschroef gekozen zijn.

[`print/controle.json`](print/controle.json) bevat de herimportcontrole;
[`print/slicercontrole.json`](print/slicercontrole.json) de proefslicing met
Bambu Studio. Geen van beide vervangt een fysieke lek-, drijf- of vaartest.
