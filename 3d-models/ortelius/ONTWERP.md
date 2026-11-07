# Ontwerp Ortelius RC — vormstudie v2

Deze versie is een **visueel browsermodel**, geen CAD-bron of printbestand.
Eerst de vorm beoordelen; de constructieve RC-uitwerking volgt daarna.
Alle geometrie staat zelfstandig in [`index.html`](index.html), met Three.js
r128 via vastgepinde CDN-links. Er is geen buildstap.

## Maten en herkomst

Maten zijn in **centimeters op modelschaal 1:100**: 1 cm model = 1 m echt.
De romplengte is nu ook geometrisch 91 cm, de maximale rompbreedte 17,2 cm
en de getekende waterlijn ligt 5,4 cm boven de kiel. De eerdere romp eindigde
bij circa 88,8 cm. Uitstekende uitrusting en veiligheidsnetten vallen buiten
de rompmaat; 91 cm is dus geen gemeten totaalmaat van alle details.

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

De 17 foto's staan lokaal in `images/ortelius-01.jpg` t/m `ortelius-17.jpg`.
Ze zijn buiten Git gehouden; het browsermodel laadt ze niet. De foto's tonen
verschillende kleurstellingen en uitrusting. De geometrie hieronder is een
vormstudie op basis van die verzameling, geen vastgelegde historische toestand.

| Referentie | Zichtbare kenmerken | Aanpassing in v2 |
|---|---|---|
| 02, 06, 08, 09 | Zijprofiel, dekniveaus, schoorsteen en sloepen | Posities herverdeeld; lage accommodatie met kleinere patrijspoorten, smaller hoger dekhuis en open gangboorden |
| 09, 10, 13 | Brugfront en brugvleugels | Kortere, gefacetteerde brug; naar boven uitlopende gevel, losse raamvakken met witte stijlen en schuine zijwangen |
| 03, 07, 11, 15 | Getrapte spiegel en open achterdekken | Lagere achterromp en twee open niveaus met kolommen en witte randliggers |
| 05, 14 | Helidek, hangaringang en veiligheidsnetten | Groter, afgeschuind helidek met open netstructuur en zichtbare hangaringang |
| 06, 09, 14 | Schoorsteenkap, uitlaten, mast en davits | Schuine witte mantel, oplopende zwarte kap, drie mastarmen en geknikte sloepdavits |
| 07, 16 | Droogdok en boeg | Oplopend onderwaterschip achter en smallere kiel; verdere onderwatervorm blijft onzeker |

De scheepsnaam is behouden. Het gekleurde embleem op de schoorsteen is
verwijderd; het model heeft geen rederijlogo's. De valreep is horizontaal
gestuwd in plaats van schuin door het water getekend.

## Assen en belangrijkste stations

- **x:** lengte, achtersteven = 0, boeg aan dek = 91.
- **y:** hoogte, kiel = 0, waterlijn = 5,4.
- **z:** breedte, middenlijn = 0; +z = stuurboord, −z = bakboord.

| Deel | x-bereik | Hoogte y | Breedte / keuze |
|---|---|---|---|
| Achterste werkvloer | 0,2–24,2 | 10,7 | Max. 16,6; afgeschuinde hoeken |
| Promenadedek achter | 0,2–24,2 | 13,9 | Max. 17,4; open ruimte eronder |
| Hoofddek voor | 24–91 | 13,9 | Volgt de rompvorm |
| Lage accommodatie | 22–76 | 13,9–16,6 | Max. 16,4 |
| Hoger dekhuis | 46–74,8 onder / 50–72,8 boven | 16,6–19,3 | Smaller; schuin oplopende achterwand |
| Brug | ca. 60–74 | 19,3–23,5 | Naar boven uitlopend; vlak front met afgeschuinde hoeken |
| Kompasdek | 59,3–74,65 | 23,8 | Max. 16,6 |
| Hangar | 21–36,5 | 16,6–19,2 | Max. 11,8 |
| Helidek | 0–21,1 | 16,75 | Max. 17,8 zonder netten |
| Schoorsteen | ca. 30,4–39,7 | 19,4–26,3 | Schuine mantel en overstekende kap |
| Sloepen | middelpunt 40,5 | onderzijde 19,45 | Twee gesloten sloepen met geknikte davits |
| Zodiacs / knikarmkranen | ca. 53 / 55,2 | op dek 19,3 | Stapels en losse oranje kranen |
| Zwarte mast | ca. 37,6 | top 38,2 | Vakwerk met drie ra's |
| Witte radarmast | ca. 64,8 | top 37,4 | Twee draaiende radars |
| Voormast | 82 | top 27,2 | Slanker en lager dan de radarmast |

## Rompvorm

`hullStations` bevat per hoogte de halve breedte en de achterste/voorste x.
`station`, `hullHW`, `hullX0`, `bowX` en `hwAt` interpoleren deze doorsnedes.
De onderste gesloten romp loopt tot de achterste werkvloer op y = 10,7.
Daarboven begint de gesloten voorromp pas bij x = 24; zo blijven achter de
bovenliggende dekken twee echte open niveaus zichtbaar.

De kiel is versmald ten opzichte van v1 en de onderkant loopt naar achteren
op. Dit is nog geen definitieve keuze voor spanten, schroefraam, stevenbuis,
roerkoker of boegschroef. De getekende aandrijving is alleen een visuele indicatie.

## Bediening en vormcontrole

Vaste aanzichten: **Driekwart, Stuurboord, Bakboord, Boeg, Achterschip,
Bovenaanzicht**. Slepen en zoomen blijven beschikbaar. Het model begint stil,
zodat de vorm direct kan worden bekeken.

- **Water:** aan = waterlijn zichtbaar, onderwaterschip afgedekt; uit = hele romp.
- **Voorgestelde deelvlakken:** alleen rode hulplijnen, geen losse CAD-delen.
- **Bovenbouw eraf:** visuele animatie van de opbouw, geen uitgewerkte passing.
- **Avond:** licht uit de ramen; **Langzaam draaien:** automatische rotatie.

Beoordeel eerst de zijprofielen en het brugfront, daarna het achterschip en
het bovenaanzicht. De pagina bevat bewust nog geen verwijzing naar een
printpakket.

## Vervolg: printbare RC-constructie

De gebruiker wil eerst dit 3D-model zien. Daarom zijn in deze stap **geen
CAD-, STL- of 3MF-bestanden** gemaakt. `cad/` en `print/` blijven gereserveerd.

Een mogelijke rompverdeling heeft sneden bij x = 22,75 / 45,5 / 68,25:
vier nominale lengtes van 22,75 cm. Dit vervangt het onjuiste eerdere totaal
van 4 × 22,5 cm voor een romp van 91 cm. Verbindingslippen, brims en
printstand moeten bij de CAD-uitwerking opnieuw op het P2S-volume van
256 × 256 × 256 mm worden gecontroleerd.

Daarna volgen: wanddiktes, echte verbindingen, toegang tot de techniek,
montage voor concreet gekozen motor/as/roer/boegschroef, gewichtsbegroting,
proefprint, slicercontrole, waterdichtheidsproef en stabiliteits-/vaartest.
Dunne relingen en antennes zijn voor de vorm getekend; ze zijn niet daarmee
als printbaar gevalideerd.

## Werken in de bron

- `loft`: doorlopende, afgeronde rompdoorsnedes en sloepen.
- `tier`, `plan`, `slab`: hoekige dekken en corresponderende gevelvlakken.
- `sidePanel`: zijwangen en schoorsteenkap uit profielpolygonen.
- `bridgeRing`, `facadeWindows`: schuine bruggevel en losse glasvakken.
- `Rods`, `railing`, `stairs`: masten, kolommen, relingen, davits en trappen.
- `viewDirections`, `positionView`: vaste camera-aanzichten.

De kleuren staan bij `NAVY`, `BOTTOM`, `WHITE`, `GLASS`, `GREEN`.
