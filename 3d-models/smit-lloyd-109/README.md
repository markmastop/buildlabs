# Smit-Lloyd 109

Printbare bovenbouw voor een RC-model van de Smit-Lloyd 109, gereconstrueerd
uit foto's en eigen metingen. De opbouw past met een los pasframe in de
dekopening van een bestaande romp en blijft afneembaar.

**Status:** versie 18, printbaar prototype. Geometrie digitaal gecontroleerd
(gesloten meshes, STEP opnieuw ingelezen, botsingen, symmetrie); nog geen
fysieke pasproef of laagcontrole in Bambu Studio.

V18 laat het onderdekhuis de vorm van de echte opbouw volgen, op basis van de
referentiefoto's `images/referentie/IMG_0297..0299`. De gemeten v17-maten
blijven gelden:

- Het blok aan de brede arm is één vlak blok op dekhoogte. De getrapte kast met
  trap (17) en de achterkasten 18/19 vervallen.
- De U-bodem is een rechte achterwand met binnenhoeken R2, zonder schuine
  hoekwangen en deur. De twee kleine ramen blijven.
- In de hoek tussen blok en arm zit een inkeping van 12 × 15 mm (fotomaat).
- De binnenkant van beide armen loopt over de laatste 40 mm schuin naar buiten
  (10 en 7 mm, fotomaat).
- Armuiteinden R8 en staande hoeken van de voorblokken R6.
- De schoorstenen en voetplaten zijn achteraan aan de binnenkant versmald, zodat
  ze binnen de schuine armrand blijven; het binnenrooster staat op dat vlak.

## Openen

- [`index.html`](index.html): overzicht met 3D-model, maten, downloads en checklist.
- [`bekijken.html`](bekijken.html): volledige 3D-kijkversie (v18, vergelijken met v17).
- [`HANDLEIDING.txt`](HANDLEIDING.txt): printen en montage, stap voor stap.

## Maten

Gemeten: onderbouwlengte 385 mm, voordekbreedte 180 mm, voordeklengte 163 mm,
dekhoogtes 60 en 86 mm, U-opening 80 × 115 mm, dekopening romp 205 × 153 mm.
Totale opbouw ca. 410 × 189 × 202 mm. Stuurhut, ramen, schoorstenen en
roosters zijn fotoreconstructies, geen bewezen schaalmaten.
Details: [`meetmaten.csv`](meetmaten.csv), [`AANNAMES.txt`](AANNAMES.txt),
[`controle.json`](controle.json).

## Bestanden

| Map / bestand | Inhoud |
|---|---|
| `CAD/` | Bewerkbare bron: `build.py` met `parameters.json` en `metingen.json`; `voetafdruk.py` (omtrek onderdekhuis, ook voor de dekmal), `validate.py` (controles), `maataanzichten.py` en `kijkmodel.py` (tekeningen en kijkmodellen) |
| `inputs/` | Nodig om de CAD opnieuw te bouwen (v4-bron, logo-SVG) |
| `STEP/` | 27 losse delen + `SL109_v18_assemblage.step` |
| `STL/` | 27 printbestanden; `onderdelen.csv` geeft aantal, maat en printstand |
| `pasmal/` | Pasproeven voor dekopening, buitenmaat en stuurhuthoogte |
| `referentie_*/` | Foto's per detail, gebruikt bij de reconstructie |
| `SHA256SUMS.txt` | Controlesommen van het oorspronkelijke printpakket |

Het volledige printpakket (`Smit-Lloyd-109_v18_printpakket.zip`)
bevat dezelfde STL- en STEP-bestanden en blijft buiten Git; verspreid het via
GitHub Releases als dat nodig is.

## Volgende stappen

1. Print [de pasproef](pasmal/00_pasproef.stl) en pas hem in de dekopening van de romp.
2. Bepaal de definitieve lengtepositie van het pasframe (nu voorlopig X = 160 mm).
3. Controleer de laagweergave in Bambu Studio en print de rest volgens
   `HANDLEIDING.txt`.

## Maatcontrole

[Bovenaanzicht met maten](beelden/bovenaanzicht-maten-v18.svg) en [zijaanzicht met maten](beelden/zijaanzicht-maten-v18.svg) staan ook op de projectpagina. Afmetingen in mm; geen afdruk op schaal. De positie van het pasframe is voorlopig. Oude wijzigingsverslagen en het oude kijkmodel zijn opgeruimd. `inputs/` bevat noodzakelijke bouwafhankelijkheden en blijft behouden.

## Visuele voorbeeldromp

De 3D-kijkversie heeft een aan/uit-schakelbare, eenvoudige donkere romp met groen dek. Dit is uitsluitend context, geen gereconstrueerde romp en geen pascontrole. Aangenomen afmetingen: circa 1080 × 244 × 128,5 mm; dek gelijk met de onderrand van de opbouw. De werkelijke rompmaat en positie zijn niet vastgesteld. De voorbeeldromp staat uitsluitend in `bekijken.html`; CAD, STEP, STL en maataanzichten blijven ongewijzigd.

Het actuele kijkmodel is direct ingebed in `index.html` en wordt bij openen geladen, zonder eerst op een kijklink te klikken. `kaart.html` (homepagekaart), `bekijken.html` en `index.html` delen hetzelfde geometrieblok.

## Opnieuw bouwen

Met Python, CadQuery 2.8, trimesh en numpy (`CAD/requirements.txt`), vanuit deze map:

1. `python CAD/build.py`: STL, STEP, assemblage, `controle.json` en `onderdelen.csv`.
2. `python pasmal/maak_pasmal.py`: dekmal uit dezelfde voetafdruk.
3. `python CAD/maataanzichten.py`: boven- en zijaanzicht in `beelden/`.
4. `python CAD/kijkmodel.py`: kijkmodellen in `kaart.html`, `bekijken.html` en `index.html`.
5. `python CAD/validate.py`: hercontrole, `SHA256SUMS.txt` en het printpakket.
