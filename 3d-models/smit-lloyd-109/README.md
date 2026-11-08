# Smit-Lloyd 109

Printbare bovenbouw voor een RC-model van de Smit-Lloyd 109, gereconstrueerd
uit foto's en eigen metingen. De opbouw past met een los pasframe in de
dekopening van een bestaande romp en blijft afneembaar.

**Status:** versie 17, printbaar prototype. Geometrie digitaal gecontroleerd
(gesloten meshes, STEP opnieuw ingelezen, botsingen, symmetrie); nog geen
fysieke pasproef of laagcontrole in Bambu Studio.

## Openen

- [`index.html`](index.html): overzicht met 3D-model, maten, downloads en checklist.
- [`bekijken.html`](bekijken.html): volledige 3D-kijkversie (v17, vergelijken met v16).
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
| `CAD/` | Bewerkbare bron: `build.py` met `parameters.json` en `metingen.json` |
| `inputs/` | Nodig om de CAD opnieuw te bouwen (v4-bron, logo-SVG) |
| `STEP/` | 31 losse delen + `SL109_v17_assemblage.step` |
| `STL/` | 31 printbestanden; `onderdelen.csv` geeft aantal, maat en printstand |
| `referentie_*/` | Foto's per detail, gebruikt bij de reconstructie |
| `SHA256SUMS.txt` | Controlesommen van het oorspronkelijke printpakket |

Het volledige printpakket (`Smit-Lloyd-109_v17_printpakket.zip`, 35 MB)
bevat dezelfde STL- en STEP-bestanden en blijft buiten Git; verspreid het via
GitHub Releases als dat nodig is.

## Volgende stappen

1. Print `00_pasproef` en pas hem in de dekopening van de romp.
2. Bepaal de definitieve lengtepositie van het pasframe (nu voorlopig X = 160 mm).
3. Controleer de laagweergave in Bambu Studio en print de rest volgens
   `HANDLEIDING.txt`.

## Maatcontrole

[Boven- en zijaanzicht met maten](beelden/maataanzichten-v17.svg) staan ook op de projectpagina. Afmetingen in mm; geen afdruk op schaal. De positie van het pasframe is voorlopig. Oude wijzigingsverslagen en het oude kijkmodel zijn opgeruimd. `inputs/` bevat noodzakelijke bouwafhankelijkheden en blijft behouden.
