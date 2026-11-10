# CAD naast de vormstudie v3

## Silhouetvergelijking van 09-11-2026

De CAD-assemblage en de vormstudie [`../index.html`](../index.html) zijn vanuit dezelfde
camerastandpunten als silhouet gerenderd en over elkaar gelegd. Grijs is gelijk, rood zit
alleen in de vormstudie, blauw alleen in de CAD.

![Overzicht](../beelden/cad-vergelijking-overzicht.png)

Romp, dekken, opbouw, schoorsteen, masten, helidek en hangar vallen binnen circa 1 mm samen.
De verschillen die overbleven:

| Verschil | Oorzaak | Aanpak |
|---|---|---|
| Boeg was een wig van circa 26 mm lang en 62 mm breed | Rompcontour met gelijke stappen in X; te grof bij de steven | Fijnere, sinusvormige verdeling in de laatste twee vakken (`bow_tip_samples`) |
| Verschansing vlak 13,5 mm | Zeeg uit de vormstudie ontbrak | 11 mm tot X=740, oplopend naar 15,5 mm |
| Voormast Ø2,6 mm, ra in de lengterichting | Vereenvoudigd voor de printstand | Taps Ø5,2 naar Ø3,2, ra dwarsscheeps, toplicht, kraag en voet |
| Grote dome, GPS en antennes aan de verkeerde zijde | Z van de vormstudie is stuurboord, Y van de CAD is bakboord | Y-teken omgedraaid |
| 4 mm kier boven de achterkajuit | Wand 25 hoog onder een dek op 29 | Wand 29 hoog |
| Wit platform onder de sloepen, zwevend en door de reling | Printhulp die niet in de vormstudie staat | Twee consoles per sloep tegen de wand |

![Boeg van boven](../beelden/cad-vergelijking-boeg-boven.png)
![Boeg van opzij](../beelden/cad-vergelijking-boeg-zij.png)
![Boeg voor en na](../beelden/cad-voor-na-boeg.jpg)
![Sloep voor en na](../beelden/cad-voor-na-sloep.jpg)

Bewust niet aangepast: stagen en vlaggenstok voorop (garen en draad), de draaiende radarbalken
(stand verschilt per moment) en de iets kleinere vlag.

## Opgelost 10-11-2026: schroef onder het achterschip

In p2 liet de romp bij de schroefnaaf maar een straal van 14,5 mm vrij, dus hooguit een
schroef van Ø29 mm, en het roerblad zat waar de schroef had moeten draaien. Het achterschip
is daarom opnieuw getekend (`stern` in `parameters.json`):

- Onder de toonbank (z 44–47 mm) loopt de romp uit in een smalle scheg, halve breedte 9 mm,
  die bij x=44 eindigt. Daar komt de stevenbuis naar buiten.
- Schroefnaaf op x=36, z=20,5. De Ø40-schroefmal blijft vrij van de romp en boven
  de kiellijn. De gemeten marges staan in de hercontrole hieronder.
- Gebalanceerd hangroer met NACA-profiel (koorde 22, dikte 30 %), voorrand op x=29, koning
  op x=23. Het roer raakt de schroefcirkel niet; `validate.py` controleert dat nu.
- De schroefas stijgt met 5,9° (helling 0,103) naar de motor; de servoplaat schuift naar x=150.
- De buitenkant is vanaf x=212 gelijk aan p2. Daarom zijn alleen `01_romp_1`, `52_servoplaat`,
  `56_roerblad` en de nieuwe schroefmal `57_schroefmal_40` veranderd.

Waterverplaatsing bij de ontwerpwaterlijn (54 mm): 4,571 kg (was 4,628); drukkingspunt op
x=411 mm.

![Achterschip voor en na in de vormstudie](../beelden/cad-voor-na-achterschip.jpg)
![Rompdeel 1 voor en na in de CAD](../beelden/cad-achterschip-romp.jpg)

## Hercontrole van de actuele STEP-bestanden op 10-11-2026

De [vormstudie v3](../index.html) bepaalt het silhouet, de zichtbare details en
de beoogde RC-indeling. Voor de vergelijking zijn haar centimeters omgerekend
naar millimeters. Hier loopt X vanaf de spiegel naar de boeg, Y is positief
naar bakboord en Z is de hoogte boven de kiellijn. De ontwerpwaterlijn ligt
op Z=54. De STEP-onderdelen zijn uit de printstand teruggezet op hun
assemblageposities. Waar CAD alleen een houder levert, is het
ruimtemodel uit v3 tegen die houder en de romp gelegd.

| Onderdeel | Verschil ten opzichte van v3 | Beoordeling |
|---|---|---|
| Romp, boeg en opbouw | Hoofdcontour, zeeg, open galerijen, brug, schoorsteen, helidek en hangar volgen v3. CAD voegt een holle printromp, lasstroken en demontabele dekmodules toe. | Behoud deze constructie. De eerdere silhouetvergelijking betreft de hoofdvorm. |
| Achterdekken | V3 heeft een blauwe promenadedekrand en korte schoren en dwarsliggers rond de kolommen. CAD geeft het dek groen weer en werkt de zichtbare ondersteuning hoofdzakelijk uit als losse rechte kolommen. | Neem de blauwe rand over in de afwerking. De schoren en dwarsliggers bepalen mee hoe open en herkenbaar het achterschip oogt. |
| Rompafwerking en fijne details | V3 toont de smalle lichte schuurlijst, beplatingslijnen, boegschroef- en diepgangmerken en de naam op de spiegel. CAD heeft gesloten patrijspoortplaatjes, losse ankers en naamplaten op het kompasdek. Relingrails en staanders zijn 1,2 en 1,4 mm dik, tegenover respectievelijk 0,6–1,2 en 0,9 mm in v3. | Neem de rompmarkeringen en spiegeltekst over als afwerking. De dikkere relingen zijn een bewuste keuze voor FDM. |
| Helikopters | V3 toont standaard één toestel op dek en één in de lucht. CAD toont beide in de hangar en levert de rotorbladen los. | Dit zijn verschillende presentatiestanden van hetzelfde modelbouwdetail. |
| Achterschip onder water | Scheg, schroefnaaf en roerprofiel volgen in beide modellen dezelfde hoofdafmetingen. V3 toont een visuele schroef, as en roerbediening. CAD bevat een schroefmal en roerblad, met een gesloten romp bij de doorvoeren. | Behoud de buitenvorm en werk de inbouw uit op de gekozen hardware. |

### Motor, koppeling en schroefas

- De beoogde aslijn loopt van de naaf op **X=36 / Z=20,5** naar de scheg op
  **X≈44 / Z≈21** en de motor op **X≈250 / Z≈42,5**, onder **5,9°**. V3 tekent
  circa 193 mm tussen de uiteinden van de stevenbuis en reserveert 15 mm
  tussen buis en motor voor de koppeling. De selectielijst noemt circa 200 mm
  en de bestelpagina noemt een as van 290 mm. Controleer de afzonderlijke
  maten van as en buis, de naaf, borgmoer en koppeling op één maatlijn.
- De **Ø60 × 100 mm motorreservering** blijft op de v3-aslijn circa **7,1 mm**
  vrij van de CAD-romp, maar overlapt de vlakke motorplaat tot **7,3 mm in
  hoogte**. De plaat staat op Z=16–20 en heeft twee langssleuven op Y=±26 mm.
  De plaat staat los van de romp in de assemblage. De bevestiging en
  uitvulling, de beugelmaat en de aansluiting op de aslijn vragen een
  motorafhankelijke uitwerking. De v3-koppeling en stevenbuis blijven vrij
  van de eerste lasstrook in de geometriecontrole.
- De MFA Torpedo 850 is een kandidaat uit de selectielijst. Het
  [MFA-datablad voor de RE-850](https://asset.conrad.com/media10/add/160267/c1/-/gl/000222377DS00/datasheet-222377-mfa-torpedo-850-brushed-elektromotor-pre-modely-lodi.pdf)
  vermeldt een huis van Ø51,8 mm, circa 110 mm totale lengte, een as van
  Ø6,35 mm, circa 595 g en 10.000 t/min onbelast bij 12 V. De term
  ‘langzaamlopend’ in v3 onderbouwt de keuze voor deze motor met een
  Ø40-schroef op 2S onvoldoende. De motoras vraagt een eigen aansluitmaat
  aan de koppeling. Bepaal de passing en het gedrag onder schroefbelasting
  met de gekozen motor, voeding en schroef.
- De **Ø40 × 6 mm schroefmal** staat in de STEP-assemblage loodrecht op X.
  Op de werkelijke aslijn gekanteld is er **3,82 mm** tot de romp en ligt
  het laagste punt circa **0,30 mm boven de kiellijn**. Dit betreft de
  mal. Neem ook de echte naaflengte en eventuele axiale verplaatsing mee.

### Roer, servo en servicetoegang

- Het roer volgt v3. De koorde is **22 mm**, de hoogte **40 mm**, de
  voorrand ligt op X=29 en de koning op X=23, circa 27% van de koorde
  achter de voorrand. De bovenzijde ligt op Z=43 en de onderzijde op Z=3.
  In middenstand blijft het blad **2,23 mm vrij van de romp** en
  **1,97 mm van de gekantelde schroefmal**. Ook op de geteste standen
  ±20°, ±35° en ±45° blijven blad, romp en mal gescheiden. De steekproef
  omvat het blad en de mal. De beweging van hevels en stang vereist een
  aparte controle.
- De huidige STEP-boring is **Ø4,2 mm**, bedoeld voor een metalen
  **Ø4 mm-roerkoning**. De oudere onderdelenlijst noemt Ø3 mm. V3 toont de
  koker tot Z=69 en de roerhevel op Z=72. De CAD-romp is op X=23 nog dicht.
  Leg vóór het boren vast welke koker, lagering, afdichting en axiale
  borging samen passen. De kokerdoorvoer in de toonbank ligt onder de
  ontwerpwaterlijn.
- De servoplaat op X=150 is in CAD aan **bakboord** gemodelleerd. In v3
  ligt het servovolume aan **stuurboord**. Aan de overeenkomstige kant
  vergeleken is het v3-volume **42 × 20 mm** in bovenaanzicht en de
  plaatopening **41 × 21 mm**. Een rechthoekig huis volgens die reservering
  is 1 mm te lang. De losse servoplaat heeft bovendien circa 17 mm afstand
  tot het dichtstbijzijnde punt van de romp. Leg de kant, de dragende
  bevestiging en de maten van huis en montageoren vast met de gekozen servo.
- De servo valt onder het serviceluik. De roerhevel op X=23 ligt **47 mm
  achter de nominale opening** (X=70–220) en de koppeling ligt net vóór
  die opening (X≈235–250). Maak de hevel en koppeling bereikbaar voor
  gereedschap en demontage, inclusief met de dekken op hun plaats. Modelleer
  de stang en beide hevels samen, zodat ook de uitslag en de bereikbaarheid
  van de borgschroeven kunnen worden gecontroleerd.

### Printstatus en eerstvolgende ontwerpbeslissing

De actuele onderdelenlijst en geometriecontrole tellen **216 unieke delen**.
Het aanwezige lokale p2-ZIP en de opgeslagen slicercontrole tellen **214**.
Het ZIP bevat het eerdere rompdeel 1 en mist de schroefmal. Het slicerrapport
gebruikt voor rompdeel 1, de servoplaat en het roer andere 3MF-hashes dan
de actuele exports en vermeldt de schroefmal nog niet. De passing hierboven
is gemeten met de actuele STEP-bestanden.

Werk eerst de **aandrijving en roerbediening als één inbouwassemblage** uit,
met de v3-buitencontour, de naaf en roerkoning op hun huidige posities.
Daarna kunnen de doorvoeren, dragende steunen en servicetoegang samen
worden gecontroleerd. Een pasproef van de complete aandrijving en
roerbediening in het achterschip kan voorafgaan aan het verlijmen van de
romp en het definitief sluiten van het achterdek.
