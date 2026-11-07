# Start hier — Ortelius RC

## Actuele opdracht en status

De gebruiker heeft de vormstudie bekeken en vraagt nu CAD- en printbestanden.
**Constructieprototype p1 is beschikbaar:** 68 unieke onderdelen met CAD-bron,
STEP, STL, geometrie-3MF, onderdelenlijst en bouwbeschrijving.

Begin met [de CAD-weergave](cad/index.html) en
[de bouw-/printvolgorde](print/BOUWHANDLEIDING.md). Print eerst de kleine
pasproefstukken. De 34 referentiefoto's blijven lokaal buiten Git.

De oorspronkelijke [vormstudie v3](index.html) blijft beschikbaar en toont
meer schilder- en modelbouwdetails dan de vereenvoudigde printgeometrie.

De viewer bevat ook **RC-inbouw**: motor, accu, as, roerservo, twee regelaars,
ontvanger en een boegschroef als ruimtereserveringen. Zie de RC-secties in
README en ONTWERP voor maten en onzekerheden. Het is geen gevalideerde inbouw.

Er zijn ook twee gele helikoptervormstudies (AS350/H125 als referentie),
met een helidek-/luchtstand en een gecontroleerde modelstalling naast
elkaar zonder hoofdrotorbladen. Gebruik **Heli’s in hangar** en
**Helikopter**; zie README/ONTWERP voor maten en beperkingen.

## Bestanden om te lezen

1. [`README.md`](README.md): status, hoofdmaten, bronnen en voorbeeldbeeld.
2. [`ONTWERP.md`](ONTWERP.md): fotokoppeling, huidige modelstations, aannames en bronfuncties.
3. [`ONDERDELEN.md`](ONDERDELEN.md): voorlopige RC-onderdelenlijst, nog geen bevestigde inbouwmaten.
4. [`referentie/README.md`](referentie/README.md): de foto's staan lokaal in `images/`, buiten Git.

## Uitgangspunten

- Lengte over alles circa 91 cm, rompbreedte 17,2 cm; waterlijn 5,4 cm boven de kiel.
- Centimeters in de vormstudie; CAD/print in millimeters.
- Eén schroef, roer en voorgenomen boegschroef; afneembare opbouw.
- Materiaal: PETG (gekozen 08-11-2026, in plaats van ASA), epoxy aan de binnenkant, 2S LiPo.
  Zie de materiaalnotitie in `ONTWERP.md`.
- Dekhoogtes, raampatronen en onderwatervorm zijn schattingen uit foto’s.
- Uitgewerkte rompsneden op 227,5 / 455 / 682,5 mm met losse interne lasstroken.
- Geen rederijlogo's. Referentiefoto's niet publiceren.

## Volgorde hierna

1. Drie pasproefstukken printen en lijmspeling beoordelen.
2. Werkelijke RC-hardware kiezen; houders en technische doorvoeren daarop aanpassen.
3. Romp en afneembare opbouw monteren volgens de bouwbeschrijving.
4. Complete massa wegen en lek-/drijfproeven doen; laag ballasten en trim controleren.
5. Elektronica inbouwen en rustig proefvaren.

De huidige digitale checks staan in `print/controle.json` en
`print/slicercontrole.json`; fysieke tests zijn nog niet gedaan.
CAD-bronnen staan in `cad/`, STL/3MF in `print/`. Het lokale ZIP-pakket wordt
met `cad/package.py` gemaakt en blijft volgens `.gitignore` buiten Git.
Commit alleen opdrachtwijzigingen; push uitsluitend op verzoek.
