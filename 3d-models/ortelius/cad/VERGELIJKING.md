# CAD naast de vormstudie (09-11-2026)

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

## Aandachtspunt: schroef onder het achterschip

In de vormstudie staat de schroefnaaf op X=35, Z=22 mm. De romp laat daar een straal van
14,5 mm vrij, dus hooguit een schroef van Ø29 mm. Voor de Ø40 mm uit de bestellijst:

| Naaf op X (mm vanaf de spiegel) | Naafhoogte Z | Vrije straal | Speling bij Ø40 |
|---:|---:|---:|---:|
| 35 | 22 | 14,5 | past niet |
| 25 | 20 | 22,5 | 2,5 mm, bladpunt op de kiellijn |
| 20 | 22 | 23,2 | 3,2 mm, bladpunt 2 mm boven de kiellijn |

Bij X=20 tot 25 zit de schroef in het huidige roerblad (X=-2 tot 22). Leg schroefaslijn,
schroefmaat en roer dus samen vast voordat de doorvoeren in de romp komen. Ø45 mm past nergens
zonder onder de kiel uit te steken.
