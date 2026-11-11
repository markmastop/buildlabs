# CrowPanel Advance 5.0 — matte PLA portretbehuizing

Versie 1 · 26 september 2026 · alle maten in millimeters.

Dit ontwerp bestaat uit drie printdelen: een frontbak, een geventileerd achterdeksel en een voet met 15° helling. De zwarte fabrieksplaten en hoekschroeven van de **CrowPanel Advance 5.0 ESP32-S3** blijven zitten. Niet ontworpen voor de nieuwere ESP32-P4-variant of een kaal printplaatje.

**Print eerst `crowpanel_fit_test.stl`.** De passing is digitaal gecontroleerd tegen ELECROW's STEP-model, maar nog niet op jouw apparaat of met jouw filament getest. Het pasframe controleert de buitenrand, schermopening en onderste ondersteuning; niet de volledige diepte of kabelgeleiding. Het is geen onderdeel van de uiteindelijke behuizing.

## Bestanden

| Bestand | Gebruik | Printmaat X × Y × Z |
|---|---|---:|
| `crowpanel_front.stl` | Frontbak met steunrand en kabelbocht | 100 × 182 × 24 |
| `crowpanel_back.stl` | Afneembaar ventilatiedeksel | 100 × 182 × 2,4 |
| `crowpanel_foot.stl` | Voet met schuine opname en open kabelgoot | 108 × 80 × 35 |
| `crowpanel_fit_test.stl` | Eerst printen voor pascontrole | 100 × 182 × 5 |
| `crowpanel_assembly.step` | Complete montage voor CAD | circa 108 × 81 × 189 |
| `crowpanel_*.step` | Afzonderlijke bewerkbare CAD-solids | dezelfde geometrie als STL |
| `crowpanel_advance5_parametric.py` | Parametrisch CadQuery-bronbestand | parameters bovenaan |
| `validation.json` | Geometrische controle en bestandschecksums | — |

STEP bevat bewerkbare solids; de ontwerpgeschiedenis/parameters staan in het Python-bronbestand. Er is geen OpenSCAD-bestand. Om opnieuw te genereren: Python 3.11 met `cadquery` en `trimesh`, daarna `python crowpanel_advance5_parametric.py nieuwe_map`. USB-positie, steunpunten en schermopening horen bij deze specifieke module; bij een ander paneel moeten die samen worden aangepast.

## Printen op de Bambu Lab P2S

De STL's staan al in de bedoelde printoriëntatie op Z=0. Importeer in millimeters, schaal 100%, automatische oriëntatie uit.

- 0,4 mm nozzle, 0,20 mm lagen, vier wanden, vijf boven- en onderlagen.
- 20% gyroid infill; support uit. Kleine bruggen bij schroefgaten en voetjesuitsparingen blijven aanwezig.
- Mat PLA-profiel passend bij het gebruikte merk. De controle gebruikte **Bambu PLA Matte @BBL P2S**.
- Buitenwand 60 mm/s voor een rustig oppervlak; overige instellingen uit het P2S-standaardprofiel.
- Front met zichtzijde op de plaat; deksel met buitenzijde op de plaat; voet met zool op de plaat.
- Voor de controle is ieder onderdeel apart gesliced. Een schone textuurplaat geeft het front een matte structuur. Brim alleen toevoegen als jouw PLA op deze plaat opkrult.

| Onderdeel | Slicerindicatie materiaal | Tijd inclusief voorbereiding |
|---|---:|---:|
| Front | 94 g | 2 u 32 min |
| Deksel | 51 g | 1 u 10 min |
| Voet | 90 g | 2 u 35 min |
| **Complete behuizing** | **235 g** | **6 u 17 min** |
| Optioneel pasframe | 34 g extra | 55 min extra |

Dit zijn schattingen, geen gemeten printresultaten. Er wordt geen G-code meegeleverd; slice de STL's in jouw eigen Bambu Studio met jouw filamentinstellingen.

## Benodigdheden en montage

Benodigd: vier M3×10 schroeven voor het deksel, twee M3×16 voor de voet, kleine koppen (maximaal Ø6 mm), vier zelfklevende rubbervoetjes Ø10 × circa 2 mm, dun zacht EVA/schuim van 1 mm en circa 5 mm. Geen inserts of moeren nodig. De blinde pilotgaten zijn Ø2,6 mm; maak M3-draad voorzichtig met de hand, desgewenst met een tap. Schroeven niet met een machine vastzetten.

1. Test het pasframe met het apparaat inclusief zwarte platen. Controleer dat het venster het zichtbare scherm vrijlaat en de USB-poort boven de centrale uitsparing valt. Niets vastklemmen of het apparaat in een te krappe opening drukken.
2. Leg het front op een zachte ondergrond. Breng circa 1 mm dikke, smalle schuimstrookjes op de binnenste steunrand aan. Laat de glas-/aanraakzone en USB-opening vrij; laat het paneel op de zwarte fabrieksrand rusten. De uitstekende hoekschroeven krijgen ruimte.
3. Plaats het paneel van achteren in de frontbak, USB-C naar beneden. Het rust op de twee onderste schouders naast de USB-opening. Gebruik een zacht passtrookje bovenaan als de kortere 134 mm-uitvoering daar beweegt.
4. Steek de USB-kabel in. Het ontwerp biedt **22 mm recht traject vanaf de poortmond** (circa 21,3 mm verticale daling bij 15° helling), daarna een bocht met **R10 mm op de kabelhartlijn**. De onderzijde van de bocht wordt ondersteund; boven/naast de kabel blijft ruimte. Leg de kabel zonder spanning door de opening in het deksel.
5. Plaats vier kleine zachte pads van circa 5 mm op de vlakke fabrieksachterplaat, bijvoorbeeld links/rechts op circa 30 mm uit het midden, ruim weg van knoppen, poorten en ventilatie. De nominale afstand tot het deksel is circa 4,8 mm. Pas de paddikte aan zodat niets rammelt en het deksel zonder kracht sluit. Geen harde druk op elektronica of glas.
6. Sluit het deksel met vier M3×10 schroeven. De twee laagste gaten op 15 mm hoogte zijn voor de bevestiging aan de voet en blijven nu vrij.
7. Schuif de gesloten behuizing in de voet. Leg de kabel in de open goot naar achteren. Bevestig met twee M3×16 schroeven via de verzonken gaten achter in de voet. De schroeven gaan door het deksel in de frontbak.
8. Plak de rubbervoetjes in de vier ondiepe uitsparingen. Zet neer en controleer dat de kabel vrij ligt en het geheel niet wiebelt.

De kabelkamer heeft een 20 mm brede passage. De digitale controle gebruikte een stekkeromhulling van 19,6 × 9,6 × 22 mm en een kabel van Ø6 mm in de bocht. Kies in de praktijk een flexibele kabel met circa 20 mm of minder uitstekende stekkerlengte. Een dikke, stijve trekontlasting kan extra ruimte nodig hebben; de werkelijke kabel is niet opgemeten. De goot is open zodat de stekker er niet doorheen hoeft te worden geregen.

Voor toegang tot reset, SD en overige aansluitingen: eerst de twee voetschroeven los, behuizing uitnemen en daarna het achterdeksel verwijderen. De enige permanent bereikbare kabelroute is USB-C.

## Mechanische onderbouwing en controle

Gebruikte primaire bronnen:

- [Officiële ELECROW-repository, productgegevens](https://github.com/Elecrow-RD/CrowPanel-Advance-5-HMI-ESP32-S3-AI-Powered-IPS-Touch-Screen-800x480): opgegeven maat 136,4 × 84,7 × 15,4 mm.
- [Officiële ELECROW STEP-bestanden](https://github.com/Elecrow-RD/CrowPanel-Advance-5-HMI-ESP32-S3-AI-Powered-IPS-Touch-Screen-800x480/tree/master/3D%20file): `advance-hmi5_0-20260116.stp`, volgens ELECROW voor V1.2, gebruikt voor de botsingscontrole.
- [Officiële Bambu P2S-aankondiging](https://blog.bambulab.com/the-icon-redefined-meet-the-p2s-a-completely-reengineered-version-of-the-ultra-productive-p1-series/): bouwvolume 256 × 256 × 256 mm.

De STEP is niet identiek aan de marketingmaat: de zwarte platen zijn 134,0 × 84,7 mm; inclusief uitstekende hoekbevestiging is de totale diepte circa 17,71 mm. De USB-C-connector ligt centraal op de korte zijde: y=40,15 in ELECROW's coördinaten, mond x≈131,945, hart z≈1,605. Het frontvenster is afgeleid van de opening in de fabrieksplaat. Er is 0,5 mm nominale speling per zijde van de hoofdopname en extra lengteruimte voor het maatverschil. Een andere revisie moet met het pasframe worden gecontroleerd.

Gecontroleerd: alle vier STL's zijn gesloten, hebben consistente oppervlakterichting, bestaan ieder uit één verbonden solid en passen ruim op de P2S. Geen overlap van de officiële hardware met front of deksel; geen overlap tussen voet en behuizing. De genoemde stekkeromhulling en Ø6 mm kabelbocht botsen niet met het front. Alle vier bestanden zijn met Bambu Studio 2.8.2.61 zonder supports gesliced, exitcode 0. De CLI geeft daarbij een melding over T65535 in de standaard Bambu-machinecode; dat is geen meshfout. Daarom worden alleen modellen en instellingen beschreven, geen printklare machinecode verspreid.

Niet fysiek getest: passing op jouw exemplaar, schroefsterkte, kantelbelasting en temperatuur. De voet is verbreed en verdiept voor een ruime basis; rubbervoetjes beperken schuiven. Mat PLA kan vervormen bij warmte: kies op de vensterbank een plek buiten sterke directe zon of radiatorwarmte. De ventilatiesleuven zijn geen garantie voor een bepaalde bedrijfstemperatuur.
