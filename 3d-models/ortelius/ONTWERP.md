# Ontwerp Ortelius RC

Alle maten in **centimeters op modelschaal 1:100** (1 cm model = 1 m echt).

## Assenstelsel (gelijk aan `index.html`)

- **x:** lengte, 0 = achtersteven, boeg bij ca. 89.
- **y:** hoogte, 0 = kiel. Waterlijn **WL = 5,4**.
- **z:** breedte, 0 = midden, **+z = stuurboord**, −z = bakboord.

## Echt schip

| | Waarde | Bron |
|---|---|---|
| Lengte over alles | 90,95–91,25 m | Oceanwide / Wikipedia |
| Breedte | 17,2–17,6 m | idem |
| Diepgang | 5,4 m | Oceanwide |
| Waterverplaatsing | 4.090 t | Oceanwide |
| Ijsklasse | UL1 / 1A | idem |
| Bouw | 1989, Stocznia Gdynia, ex *Marina Svetaeva* | Wikipedia |
| Voortstuwing | één Sulzer-diesel, één schroef | Wikipedia |
| Sloepen | 2 (één per zijde) | dekplan |
| Zodiacs | 10 | Oceanwide |
| Helidek | dek 6, achterschip | Oceanwide FAQ |

Uit de foto's afgeleid (schatting): vrijboord ca. 8,5 m, dak brug ca. 18,4 m
boven WL, top masten ca. 30 m boven WL.

## Romp

- Hoofddek (bovenkant romp): **MAIN = 13,9**, vlak doorlopend (geen verhoogde bak).
- Halve breedte: `8,6 × (0,7 + 0,3 × sin(min(y/4, 1) × π/2))` → 8,6 vanaf y = 4.
- Achtersteven: spiegel, onderaan teruggetrokken: `x0 = 2,4 × (1 − min(y/5, 1))`.
  Breed achterschip (breedtefactor 0,8 op de spiegel).
- Boeg: hellende voorsteven, `bowX = 82 + 6,8 × (y/13,9)^0,85` → 88,8 aan dek.
  Taps toelopend vanaf 58% van de lengte.
- Kleuren: romp marineblauw `#1e3570`, onderwaterschip rood-oranje `#c2452d`, dekken groen `#3d6b4f`.
- Witte schuurlijst hoog op de romp (y 12,2–12,42); naam ORTELIUS op bug en achterschip erboven.
- Beplating: horizontale naden op y = 9,4 en 12,7, verticale spanten om de 6,4,
  diagonalen in de vlakken voor (x > 60) en achter (x < 20).
- Patrijspoorten: rij op y = 11,1 (x 14,5–80, steek 2,2) en losse rij op y = 7,9.
- Witte verschansing op het voordek vanaf x = 68, hoogte 1,2.
- Valreep schuin langs beide zijden van x = 20,5 (dek) naar x = 12 (y ≈ 6,3).

## Bovenbouw

| Deel | x | y | halve breedte |
|---|---|---|---|
| Achterste dekhuis (1 dek) | 15 – 38,6 | 13,9 – 16,6 | 8,3 |
| Voorste blok (2 dekken) | 38 – 70 | 13,9 – 18,6 | 8,3 |
| Brugdek | 50 – 69,8 | 18,6 – 23,4 | 7,9 |
| Brugdak / kompasdek | 49,4 – 70,1 | 23,4 – 23,7 | 8,1 |
| Hangar (op achterste dekhuis) | 15,5 – 34,5 | 16,6 – 19,2 | 5,6 |
| Schoorsteen (wit, op hangardak) | 25,5 – 32,8 | 19,2 – 26,0 | 2,8 |
| Schoorsteenkap (donker) | 25,0 – 33,3 | 26,0 – 26,7 | 3,15 |
| Helidek (groen, op kolommen, witte rand 1,1) | −1,3 – 15,7 | bovenkant 16,75 | 8,8 |

- Ramen: twee rijen op y = 15,2 en 17,4 in het voorste blok, ook in het
  front; brugramen rondom op y 20,9–22,5 met stijlen en zonnekap; naambord
  ORTELIUS op het brugfront.
- Blauwe dekzeilen achter de schoorsteen (x 18–24).

## Uitrusting

| Onderdeel | Positie | Opmerking |
|---|---|---|
| Sloep (dicht, oranje) | x 33,2, z ±9,25, onderkant y 19,55 | 8,4 lang, aan oranje A-davits op x 29,9 en 36,5 |
| Zodiacs | x 43,5, z ±3,4 op het voorste blok | stapels van 3, 5 cm lang |
| Oranje knikarmkranen | x 47,5, z ±6,6 | giek naar achteren |
| Reddingsboot + davit | x 22,5, z ±6,6 op het dekhuis | rood-oranje |
| Vakwerkmast (zwart) | x 31,6 op de schoorsteen, tot y ≈ 37,8 | twee ra's |
| Radarmast (wit) | x 56,8 op het brugdak, tot y 37,4 | radars op y 27,8 en 30,8 |
| Mastje brugfront | x 68,4, tot y 30,4 | koepels en ra |
| Voormast met tuien | x 80, tot y 28,5 | scheepsbel |
| Ankerlieren | x 82, z ±2 | kettingen naar klusgaten x 84,5 |
| Satcom-koepels | x 61,5 en 64,5 op het brugdak | 4 stuks |
| Vlag (NL) | helidekrand, x −1, z 6,5 | |

## Aanpassingen op basis van 17 foto's (`images/`)

- Hangar toegevoegd op het achterste dekhuis, met donkere deur naar het helidek;
  schoorsteen, vakwerkmast, sloepen en dekzeilen staan één dek hoger op het hangardak.
- Helidek met dikke witte rand en schuin aflopende veiligheidsnetten in plaats van reling.
- Onderwaterschip rood-oranje, romp helderder marineblauw, witte schuurlijst.
- Reddingsboot naast de hangar; trap van dekhuis naar hangardak.

## Printopdeling (Bambu Lab P2S, 256 mm)

- **Romp:** 4 delen, naden op x = 22,5 / 45 / 67,5. Elk deel max. 22,5 × 17,2 × 13,9 cm.
- **Achterste dekhuis:** 1 deel (23,6 cm).
- **Voorste blok:** 2 delen (naad rond x = 54, verspringend t.o.v. rompnaad 45/67,5).
- **Brugdek + dak:** 1 deel.
- **Schoorsteen, helidek, masten, sloepen, kranen:** los, kleine onderdelen
  in de AMS-kleuren. Relingen en antennes in messingdraad 0,8 mm.

## Open punten (verfijnen)

- Lengte over alles is in het model ca. 89 cm (+1,3 helidek-overstek);
  echt 91 cm. Boeg iets verlengen of romp schalen.
- Exacte dekhoogtes, aantal en ritme van de ramen per dek.
- Vorm van het brugfront (vlak of licht schuin) en de brugvleugels.
- Positie en vorm van de schoorsteen t.o.v. de sloepen.
- Onderwaterschip: bulbsteven aanwezig of niet; vorm van de kim.
- Logo op de schoorsteen bewust neutraal (alleen ring).

## Werken in index.html

Alle geometrie staat in het eerste grote `<script>`-blok, in deze secties
(zoek op de kopjes in het commentaar):

- `taper` / `loft`: bouwen een romp of blok uit horizontale doorsnedes
  (`x0`, `x1`, halve breedte `hw`, boegovergang `ts`, spiegel `ss`/`sf`).
- `Hull`: rompfuncties `hullHW`, `hullX0`, `bowX`, constante `MAIN`.
- `Superstructure`: `block(y0, y1, x0, x1, hw, kleur)` en de constanten
  `A1 = 16,6`, `A2 = 18,6`, `B2 = 23,4`, `CD = 23,7` (dekhoogtes).
- `Funnel`, `Helideck`, `lifeboats`, `Zodiacs and orange cranes`, `Masts`,
  `Foredeck`, `Accommodation ladder`, `Railings`, `stairs`.
- `Rods`: verzamelt staafjes (relingen, davits, tuien) in één mesh per kleur.

Kleuren staan bovenaan als constanten (`NAVY`, `GREEN`, `WHITE` …).
