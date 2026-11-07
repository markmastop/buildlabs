# Start hier (nieuwe chat)

Dit bestand is het overdrachtsdocument. Begin een nieuwe chat met de tekst
hieronder, zodat de assistent direct de juiste context heeft.

## Prompt om te plakken

> Ik bouw een RC-model van het poolexpeditieschip Ortelius, schaal 1:100
> (91 cm), om te 3D-printen op mijn Bambu Lab P2S met AMS. Alles staat in
> `~/Github/buildlabs/3d-models/ortelius/`. Lees eerst `START-HIER.md`,
> `ONTWERP.md` en `ONDERDELEN.md`, bekijk de foto's in `referentie/` en volg
> `AGENTS.md` in de root van de repo. Vandaag wil ik: **[verfijnen /
> CAD-romp maken / onderdelen bestellen / …]**.

## Waar staan we

- **Fase:** conceptmodel klaar en vergeleken met foto's (`index.html`).
- **Nog niet gedaan:** printbare CAD, wanddiktes, naden, motor- en
  roerbevestiging, waterdichtheidstest.
- **Gekozen:** schaal 1:100, romp in 4 delen van 22,5 cm, bovenbouw met
  magneten afneembaar, één schroef + roer + boegschroef, ASA, 2S LiPo.

## Twee sporen

### 1. Ontwerp verfijnen (in `index.html`)

1. Leg de foto's uit `referentie/` naast het model en noteer afwijkingen in
   `ONTWERP.md` onder *Open punten*.
2. Pas de maten aan in `index.html`; zie *Werken in index.html* in
   `ONTWERP.md` voor waar alles staat.
3. Controleer visueel (draaien, inzoomen, knoppen *Water* en *Bovenbouw eraf*).
4. Werk `ONTWERP.md` bij als maten veranderen, en commit.

### 2. Gaan bouwen (CAD en printen)

Volgorde die we hebben afgesproken:

1. **Romp in CAD** (Fusion 360 of Onshape) op basis van de rompmaten in
   `ONTWERP.md`. Wanddikte 2–2,4 mm (4 wanden ASA), overlappende naad van
   10 mm met uitlijnpennen.
2. **Inbouw ontwerpen:** motorbok, stevenbuis-ondersteuning, roerkoker,
   boegschroeftunnel van 20 mm, accubak midscheeps.
3. **Proefprint** van het achterste rompdeel (meest complex), epoxy binnenin,
   waterdichtheid testen in bad.
4. Overige rompdelen, dan bovenbouw in delen (zie *Printopdeling*).
5. Elektronica inbouwen, ballasten tot waterlijn op 5,4 cm, eerste vaartest.

Sla CAD-bestanden op in `cad/`, STL/3MF in `print/`.
