# Printbestanden — Ortelius p1

Eerste constructieprototype op 1:100 voor de Bambu Lab P2S, in millimeters.
**Begin met de pasproef; dit pakket is nog niet fysiek geprint of gevaren.**

- [`BOUWHANDLEIDING.md`](BOUWHANDLEIDING.md): printinstellingen, montage, RC-keuzes en proefvolgorde.
- [`onderdelen.csv`](onderdelen.csv): uniek onderdeel, aantal en printmaten.
- [`onderdelen.json`](onderdelen.json): montageposities, volumes, geometrische massa en geschatte waterverplaatsing.
- [`controle.json`](controle.json): onafhankelijke CAD/mesh-hercontrole.
- [`slicercontrole.json`](slicercontrole.json): uitkomsten van de proefslicing.
- [`SHA256SUMS.txt`](SHA256SUMS.txt): checksums van STEP/STL/3MF.
- `stl/`: één gesloten mesh per uniek onderdeel, in printstand.
- `3mf/`: dezelfde geometrie in expliciete mm; geen ingebakken machineprofiel of G-code.
- `profielen/`: eigen startwaarden voor romp en details; erven van het officiële P2S-procesprofiel.
- [`../cad/index.html`](../cad/index.html): de werkelijke CAD-geometrie bekijken.
- [`../cad/README.md`](../cad/README.md): parametrische bronnen en STEP-bestanden.

De kopieën en losse reling-/montagestrips staan in de onderdelenlijst.
Print op 100% en schaal niet automatisch naar de plaat. De grootste delen
zijn 240 mm lang; geometrie ≤246 mm in alle assen. Slicerhulpgeometrie,
krimp, hechting en ondersteuningen moeten ook bij jouw instellingen passen.
Print in PETG op Textured PEI Plate (op gladde PEI eerst lijmstift als scheidingslaag).

De romp blijft bij technische doorvoeren dicht totdat je de echte hardware
hebt gekozen. De proeftunnel is geen werkende boegschroef. Ramen, dekmarkeringen,
relingen en kleine aankleding vragen schilder- en modelbouwwerk. Geen
geprinte motoren, accu's, elektronica, assen of lagers inbouwen als functionele
onderdelen; de geprinte RC-delen zijn montagevoorzieningen.
