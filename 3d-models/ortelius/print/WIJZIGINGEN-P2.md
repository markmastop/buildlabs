# Verschil met p1

P2 herstelt het detailniveau uit de vormstudie. De actuele lijst bevat 214 unieke onderdelen en 355 exemplaren, inclusief reserves en pasproeven.

## Ongewijzigd en herbruikbaar

56 STL-bestanden zijn byte-identiek aan p1, waaronder 01_romp_1, 01_romp_2, 01_romp_3, 01_romp_4. Deze rompdelen hoeven bij een bestaande p1-print niet opnieuw.

## Gewijzigde bestaande delen

- `10_accommodatie_3`
- `24_helidek`
- `32_ra_1`
- `32_ra_2`
- `32_ra_3`
- `33_radarmast`
- `44_bank`
- `60_heli_romp_SB`
- `60_heli_romp_BB`

## Nieuwe details

149 unieke onderdelen zijn toegevoegd. Zie [detailvergelijking](../cad/DETAILS.md) en [actuele onderdelenlijst](onderdelen.csv) voor plaats en aantallen. Oude vlakke mast en generieke davits/kranen zijn vervangen door de ruimtelijke/gedetailleerde delen. De twee rechte relingstroken zijn reserve.

## Aanvulling 09-11-2026: CAD naast de vormstudie gelegd

De CAD is met silhouetten (zij, boven, voor, achter) over de vormstudie gelegd; zie
[de vergelijking](../cad/VERGELIJKING.md). Zeven onderdelen zijn daarna aangepast:

- `01_romp_4`, `04_hoofddek_3`, `06_bakverschansing`: ronde voorsteven in plaats van een wig;
  de verschansing heeft nu de zeeg van de vormstudie (11 naar 15,5 mm).
- `34_voormast`: taps en dikker, ra dwarsscheeps, toplicht, kraag voor de stagen, lijmvoet.
- `23_achterkajuit`: 29 mm hoog, sluit nu aan op het promenadedek (was 4 mm kier).
- `39_sloepbok_BB` en `39_sloepbok_SB` (nieuw, 2 per zijde) vervangen `39_sloepenplatform`.
- Grote satcomdome, GPS en antennes op het kompasdek stonden gespiegeld; alleen de plaats is gecorrigeerd.

`01_romp_1` t/m `01_romp_3`, de lasstroken en de pasproeven zijn ongewijzigd en hoeven niet opnieuw.
De onderdelenlijst heeft een kolom voor de massa in PETG.

**Nog te doen:** de slicercontrole in `slicercontrole.json` is voor deze zeven delen verouderd.
Draai op de Mac `cad/slice_check.py 01_romp_4 04_hoofddek_3 06_bakverschansing 23_achterkajuit 34_voormast 39_sloepbok_BB 39_sloepbok_SB`
(of de volledige controle) voordat `cad/package.py` weer een pakket maakt.

## Aanvulling 10-11-2026: achterschip met schroefopening

Zie [de vergelijking](../cad/VERGELIJKING.md#opgelost-10-11-2026-schroef-onder-het-achterschip).

- `01_romp_1`: nieuw achterschip met scheg en ruimte voor een schroef van Ø40.
  Vanaf x=212 is het deel gelijk aan p2, dus het sluit ongewijzigd aan op `02_lasstrook_1` en `01_romp_2`.
- `52_servoplaat`: verplaatst naar x=150, hoger (z=58), omdat het achterschip smaller afloopt.
  Het printbestand zelf is gelijk gebleven.
- `56_roerblad`: profielroer, wordt staand geprint.
- `57_schroefmal_40` (nieuw): ring van Ø40 × 6. Schuif deze op de as om de speling naar de romp te controleren.

`01_romp_2` t/m `01_romp_4`, de lasstroken en alle overige delen zijn ongewijzigd.

**Nog te doen:** de slicercontrole draaien voor deze vier delen. Doe dit op de Mac:
`cad/slice_check.py 01_romp_1 52_servoplaat 56_roerblad 57_schroefmal_40`

