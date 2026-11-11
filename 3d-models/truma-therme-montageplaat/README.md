# Truma Therme-montageplaat

[Open de projectpagina](index.html)

Montageplaat voor de bediening van een Truma Therme. De v17 heeft een
halfronde kabeluitsparing met straal 5,5 mm aan de zijde tegenover de knop.
Het ontwerp is gebaseerd op de aangeleverde foto's en pasvormfeedback.
Schaal 1:1. De STL meet 78 × 61 × 29 mm en past binnen het bouwvolume van
de Bambu Lab P2S.

## Bestanden

- [Print-STL v17](print/truma_bracket_cable_radius_R5_5.stl) is identiek aan de
  laatst geleverde `truma_bracket_v17.stl`.
- [Basis-STL v10](cad/truma_bracket_base_v10.stl) en
  [generatiescript](cad/build_truma_v17.py) vormen samen de bron voor v17.
  De basis is een mesh. Het script voegt de kabeluitsparing toe.
- [Render](beelden/montageplaat-v17.png) toont de v17-STL.

Met Python, `trimesh` en `manifold3d` maak je de STL opnieuw met
`python cad/build_truma_v17.py /pad/naar/truma_bracket_v17.stl`.

De oorspronkelijke v17-STL heeft niet-manifold randen. Controleer de
sliceruitvoer vóór het printen. De fysieke pasvorm is nog onbevestigd. Controleer bij een proefprint de
schroefgaten, de passing van het bedieningspaneel en de kabeluitsparing.
