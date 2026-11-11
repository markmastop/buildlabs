# EnergyDeck 7-inch behuizing

[Open de projectpagina](index.html)

Een 3D-geprinte bureaustandaard met behuizing voor het **ELECROW CrowPanel
Advance 7.0 HMI ESP32-S3 IPS-touchdisplay**, model **DIS02170A** (800 × 480).
Het display staat in portretstand. Het voorframe schuift vanaf rechts op de
behuizing en wordt bovenaan vastgezet met een losse borgclip.

## Status en maten

Printprototype **v9**, digitaal gecontroleerd volgens de meegeleverde
modelrapporten. De fysieke pasvorm van deze versie is niet bevestigd.

- Schaal 1:1. Het model gebruikt millimeters.
- Voet 126 × 120 mm, hoogte met voorframe circa 232 mm, helling 18° achterover.
- Twee steunbalkjes van 10 mm hoog, USB-doorgang van 30 mm breed en nominale
  schuifspeling van 0,25 mm per zijde.
- Maatvoering gebaseerd op het fabrikantmodel van de DIS02170A
  (`00-7_0-view-v2_12_10.stp`), eigen foto's en de opgegeven steunhoogte.
  De ruimte voor de haakse USB-C-adapter is een ontwerpaanname.

## Bestanden

| Map | Inhoud |
|---|---|
| [print](print/) | Zeven STL-bestanden voor de behuizing, het frame, de borgclip en vier pasproeven |
| [cad](cad/) | STEP-bestanden per onderdeel en van de assemblage |
| [cad/broncode](cad/broncode/) | Meegeleverde CadQuery-scripts voor de basis met gesloten USB-bodem |
| [beelden](beelden/) | Ontwerprender en details van de geleiders en steunbalkjes |
| [documentatie](documentatie/) | Oorspronkelijke handleiding en digitale controlerapporten |

Gebruik voor v9 de meegeleverde STEP van de behuizing. De CadQuery-scripts
genereren de eerdere basisgeometrie zonder de 48 afbreeksteunen van v9.

## Volgende stappen

1. Print de kleine pasproeven voor de geleiders, de borgclip en de USB-C-adapter.
2. Print de behuizing rechtop op de voet. Controleer in de slicer de 48
   meegetekende afbreeksteunen en knip die na het printen aan beide uiteinden los.
3. Plaats display en adapter via de open voorkant. Schuif het frame vanaf
   rechts op de behuizing en zet het vast met de clip.
