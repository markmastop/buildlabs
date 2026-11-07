# Start hier — Ortelius RC

## Actuele opdracht en status

De bestemming is een printbaar RC-model op schaal 1:100 voor de Bambu Lab
P2S met AMS. **De gebruiker wil eerst het verbeterde 3D-model zien.**
Werk dus eerst aan de zichtbare vorm; CAD- en printbestanden volgen daarna.

Vormstudie v2 staat in [`index.html`](index.html), met zes vaste aanzichten.
Brug, raamverdeling, open achterdekken, helidek, schoorsteen en davits zijn
verfijnd op basis van de lokale foto's. Het model is nog niet door de
gebruiker beoordeeld. Er zijn nog geen printbare CAD-delen gemaakt.

## Bestanden om te lezen

1. [`README.md`](README.md): status, hoofdmaten, bronnen en voorbeeldbeeld.
2. [`ONTWERP.md`](ONTWERP.md): fotokoppeling, huidige modelstations, aannames en bronfuncties.
3. [`ONDERDELEN.md`](ONDERDELEN.md): voorlopige RC-onderdelenlijst, nog geen bevestigde inbouwmaten.
4. [`referentie/README.md`](referentie/README.md): de foto's staan lokaal in `images/`, buiten Git.

## Uitgangspunten

- Romp 91 × 17,2 cm, getekende waterlijn 5,4 cm boven de kiel.
- Centimeters in het browsermodel; toekomstige printbestanden in millimeters.
- Eén schroef, roer en voorgenomen boegschroef; afneembare opbouw.
- Bestaande materiaalrichting: ASA, epoxy aan de binnenkant, 2S LiPo.
- Dekhoogtes, raampatronen en onderwatervorm zijn schattingen uit foto’s.
- Voorlopige rompsneden op 22,75 / 45,5 / 68,25 cm; nog geen echte verbindingen.
- Geen rederijlogo's. Referentiefoto's niet publiceren.

## Volgorde hierna

1. Vorm bekijken en eventuele correcties verwerken.
2. Parametrische CAD maken: holle romp, verbindingen, toegang en RC-inbouw.
3. Alle delen met marges controleren op het P2S-volume van 256 mm per as.
4. Gewicht/stabiliteit berekenen; pasproef en slicercontrole uitvoeren.
5. Waterdichtheid testen, elektronica inbouwen, ballasten en proefvaren.

Bewaar CAD-bronnen in `cad/` en toekomstige STL/3MF in `print/`.
Volg de werkafspraken in `../../AGENTS.md`; commit alleen wijzigingen van
de eigen opdracht en push uitsluitend op verzoek.
