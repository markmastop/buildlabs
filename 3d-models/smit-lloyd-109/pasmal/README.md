# Pasmal Smit-Lloyd 109 voor de Bambu Lab P2S

De vlakke mal volgt het plaatsingsvoorstel van 380 × 200 mm. De grondvorm rond
de neus en achteruitsparing is schematisch. Gebruik de mal om de ruimte op het
dek en de plaats van de opbouw te beoordelen.

| Printbestand | Buitenmaten |
| --- | --- |
| [Voorste helft](pasmal-voor.stl) | 190 × 196,25 × 2,9 mm |
| [Achterste helft](pasmal-achter.stl) | 190 × 200 × 2,9 mm |
| [Losse pasproef voor de dekopening](00_pasproef.stl) | 212 × 160 × 8 mm inclusief flens |

1. Print de twee helften vlak zoals ze openen, op 100% schaal. Gebruik
   bijvoorbeeld PLA, laaghoogte 0,2 mm, drie wanden en 15% vulling. De vlakke
   helften hebben geen supports nodig. Print ze ieder op een eigen plaat.
2. Leg de rechte naden tegen elkaar met de verhoogde markeringen boven.
   Lijn de buitenranden bij de naad uit en plak de helften op een vlakke
   ondergrond met schilderstape aan elkaar. Controleer 380 mm totaal.
3. Test de losse pasproef in de opening van 205 × 153 mm met de insteekrand
   omlaag. Die rand meet 204 × 152 mm en steekt 6 mm onder de flens uit.
4. Plaats de mal boven de pasproef met het voorblok naar de boeg. De vier
   ronde gaatjes geven de voorlopige buitenhoeken van de insteekrand aan.
   Kijk van boven of ze met de hoeken overeenkomen en zet de delen tijdelijk
   vast met tape als je ze samen wilt oppakken. Schuif de mal zo nodig op
   het dek en meet hoeveel de werkelijke opening afwijkt van de gaatjes.
5. Controleer de breedte bij de schoorstenen, de afstand tot de verschansing
   en het voorblok. De twee lange ribjes markeren de uiteinden van de
   stuurhutvoet. De korte ribjes op de achterarmen markeren de lengtepositie
   van de schoorsteenvoeten. Meet voor de CAD-correctie de afstand van de
   voorpunt tot de voorrand van de dekopening en eventuele zijdelingse offset.

De mal controleert de beschikbare ruimte in bovenaanzicht. Voor hoogte,
helling en een gebogen dek zijn metingen op de romp nodig. De STL's zijn
digitaal gecontroleerd op afmetingen, gesloten geometrie en één aaneengesloten
deel per bestand. De fysieke pasproef gebeurt op jouw romp.

De CAD-bron voor de mal staat in [maak_pasmal.py](maak_pasmal.py).

## Hoogtemal voor de stuurhut

Print de [hoogtemal](hoogtemal-stuurhut.stl) en de [losse voet](hoogtemal-voet.stl)
plat op 100%, zonder supports. De mal is 157 × 34 mm en de voet 46 × 40 mm.
Steek het onderste uiteinde door de voet tot het gelijk ligt met de onderkant.
Zet de voet direct op het rompdek, naast de gemarkeerde stuurhutpositie.
De vlakke pasmal eronder zou de meting verhogen.

- **86 mm** bij de onderste inkeping is de bovenkant van het verhoogde voordek.
- **141 mm** bij de bovenste inkeping is de bovenkant van de stuurhutwand.
- **157 mm** aan de bovenrand is het hoogste punt van het stuurhutdak.

Dit zijn de huidige v17-hoogtes. De stuurhut inclusief dak steekt daarmee
71 mm boven het verhoogde voordek uit. De maatvoering gaat uit van een vlak
rompdek ter hoogte van de stuurhut. Beide STL's zijn digitaal gecontroleerd.
De bewerkbare bron is [maak_hoogtemal.py](maak_hoogtemal.py).
