# Ortelius p3 · motorsteun en aandrijving

Pasmodel op schaal 1:100, in millimeters. De maatvoering volgt de bestaande
vormstudie v3 en de romp van p2. De as loopt 5,88° omhoog vanaf het
schroefvlak op X=36 / Z=20,5. Dit is de eerste p3-uitwerking van de aandrijving.

## Bekijken in Fusion

Open [ortelius-p3-aandrijving.step](ortelius-p3-aandrijving.step) via
**File → Open → Open from my computer**. Gebruik de oogjes in de Browser om
de referentieromp en het achterdek te verbergen. Kies **Inspect → Section
Analysis** voor een doorsnede door de hartlijn. De assemblage bevat de
twee achterste rompdelen, de lasstrook, het achterdek, het roer, de
printdelen en de ruimte voor de handelsdelen. De onderdelen zijn benoemd
met `PRINT`, `KOOP`, `RESERVE`, `REFERENTIE` of `MAATVOORSTEL`. De parametrische bron staat in
[build.py](build.py) en [maten.json](maten.json).

## Maatbasis

| Handelsdeel | Maten gebruikt in CAD |
|---|---|
| Krick MAX Power 600 (42124) | Huis Ø36 × 57 mm, as Ø3,17 × 8 mm en twee M3-schroeven op 25 mm hartafstand |
| Raboesch 301-24 | Buis Ø6 × 200 mm, RVS-as Ø4 × 236 mm, draad M4 × 16 en lagerhuis Ø10,5 mm |
| Navy 1482 | Koppeling Ø9 × 23 mm met boringen Ø3,17 en Ø4 mm |
| Raboesch 156-05 | Driebladsschroef Ø40 mm, naaf Ø9 × 16 mm, M4 |

Bronnen voor de maatvoering: [MAX Power 600](https://www.schiffsmodelle-shop.de/MAX-Power-600-Brushed-Motor-12V),
[montagematen motor](https://www.tecnimodel.com/en/500600-motors/11489-max-power-600-brushed-motor.html),
[Navy 1482](https://www.schiffsmodelle-shop.de/navy-Gelenkkupplung-Stahl-317-4) en
[Raboesch-catalogus, pagina's 5 en 22](https://www.bauer-modelle.com/media/9a/d6/31/1734614763/RABOESCH_CATALOGUS-2022.pdf?ts=1734614763).

De bladzone is een voorlopige draai-envelop van Ø40 × 8 mm met aparte naaf.
Het bladprofiel en de axiale bladpositie zijn niet bemaat in de geraadpleegde
catalogus. Het naafmidden ligt voorlopig 2,5 mm vóór het schroefvlak om
ruimte tot het roer te houden. De axiale positie van de schroefas, de lengte
van het lagerhuis, de ruimte voor borging en de insteekdiepten zijn ook
ontwerpwaarden. Controleer ze op de geleverde onderdelen. Het motorvlak komt nominaal op X≈288 mm,
met de koppeling voor het vaste achterdek en onder de afneembare
vooropbouw. Het gedrag van de motor op 2S met deze schroef vraagt een proef
onder belasting in het water.

De stevenbuis begint net binnen de scheg. De assemblage bevat daarom een
maatvoorstel voor een messing doorvoerbus van Ø12 × 12,5 mm met een
Ø6,2 mm zitting voor de stevenbuis. Een uitsparing van Ø10 × 7,3 mm
laat de naaf en borgmoer draaien. De bus en de stevenbuis moeten
waterdicht op elkaar en op de scheg worden aangesloten. Controleer de
werkelijke naaf, moer en resterende schegdikte vóór de bus wordt gemaakt
en de romp wordt geboord.

## Printdelen en montage

| Onderdeel | CAD | Printbestand |
|---|---|---|
| Motorsteun met schuine aslijn en open flens | [STEP](motorsteun.step) | [STL](motorsteun.stl) |
| Lijmvoet stuurboord | [STEP](lijmvoet-stuurboord.step) | [STL](lijmvoet-stuurboord.stl) |
| Lijmvoet bakboord | [STEP](lijmvoet-bakboord.step) | [STL](lijmvoet-bakboord.stl) |
| Tijdelijke uitlijnmal met twee pasboringen | [STEP](uitlijnmal.step) | [STL](uitlijnmal.stl) |

1. Print de steun met de vlakke voet op het bed. De lijmvoeten staan in
   printstand met hun vlakke bovenzijde op het bed. Controleer de eerste
   laag en de kwaliteit van de boringen in de uitlijnmal.
2. Monteer de motor met twee M3-schroeven in de voorflens. Kies schroeflengte
   op basis van de flensdikte van 5 mm en de toegestane inschroefdiepte van
   de geleverde motor.
3. Zet de steun met vier M3-schroeven op de lijmvoeten. De sleuven geven
   ±5 mm langs de as. De proefboringen in de voeten zijn Ø4,2 × 6 mm voor
   M3-inzetmoeren. Stem de boring af op je eigen inzetmoer. Dunne,
   gelijkmatige vulplaatjes onder de steun kunnen de ashoogte corrigeren.
4. Pas de stevenbuis en lijn de twee assen uit met de mal. Zet de lijmvoeten
   pas daarna vast. De voeten volgen digitaal de binnenhuid van rompdeel 2,
   met 0,35 mm verticale lijmspeling. Houd de as en de M3-boringen lijmvrij.
5. Verwijder de uitlijnmal, monteer de echte koppeling en draai de schroef
   met de hand rond bij alle roerstanden. De boring in de referentieromp
   laat de voorlopige positie zien. Controleer het echte beslag en de vrije ruimte vóór het
   boren of vastlijmen. Doe daarna een lekproef en een proef onder belasting.

Genereer de STEP- en STL-bestanden opnieuw met
`python ortelius/cad/aandrijving/build.py` vanuit de 3D-modelmap. Dit gebruikt
de [CadQuery-omgeving van het bestaande model](../README.md#opnieuw-genereren).

## Digitale controle

De Fusion-STEP is heringelezen als 17 geldige volumes. De vier losse
STEP/STL-paren hebben overeenkomstige buitenmaten en gesloten STL-meshes.
De steun meet 78 × 60 × 42 mm in printstand. De montage is gecontroleerd
in middenstand en op beide einden van de sleuven.

De voorlopige bladzone blijft 3,63 mm vrij van de romp, 0,97 mm vrij van het
roer in middenstand en 0,20 mm boven de kiellijn. Het bladvolume blijft
vrij op de geteste roerstanden van −45° tot +45°. De naaf heeft in
middenstand 1,07 mm afstand tot het roer. De werkelijke schroef en borging
bepalen hoeveel van die ruimte bij montage overblijft.
