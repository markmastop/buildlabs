# Werkafspraken voor agents

Deze afspraken gelden voor de hele repository.

## Structuur

- Elk project staat in een eigen map binnen de juiste categorie, bijvoorbeeld
  `3d-models/<projectnaam>/`. Gebruik kleine letters en koppeltekens voor
  mapnamen.
- Elk project heeft een `README.md` met: wat het is, de status, belangrijkste
  maten of keuzes, de bestanden en de volgende stappen.
- Voeg een nieuw project ook toe aan de tabel in de hoofd-`README.md`.
- Schrijf documentatie en commitberichten in het Nederlands.

## 3D-modellen

- Conceptmodellen zijn één zelfstandig `index.html`-bestand met three.js via
  een vastgepinde CDN-versie. Geen buildstap nodig.
- Maten in de modellen zijn in centimeters op modelschaal. Vermeld de schaal en
  de bron van de maten in de README van het project.
- Printbare onderdelen passen binnen het bouwvolume van de Bambu Lab P2S
  (256 × 256 × 256 mm). Houd marge en deel grotere delen op.
- Bewaar CAD-bronbestanden naast de geëxporteerde STL/3MF, zodat onderdelen
  later aangepast kunnen worden.
- Gebruik geen logo's of merkuitingen van derden in modellen; houd die neutraal.

## Automatisch committen

- Commit na iedere afgeronde wijzigingsopdracht automatisch alle wijzigingen
  die bij die opdracht horen. Vraag hiervoor niet opnieuw om toestemming.
- Gebruik een duidelijke commitomschrijving die vermeldt wat is gewijzigd en
  waarom. Voeg bij grotere wijzigingen een toelichting en uitgevoerde controles
  toe aan de commitbeschrijving.
- Controleer vóór het committen de diff en voer passende controles uit.
- Neem geen sleutels, lokale configuratie, dependencies, buildbestanden of andere
  via `.gitignore` uitgesloten bestanden op. Gebruik geen `git add -f` hiervoor.
- Laat bestaande wijzigingen die buiten de opdracht vallen ongemoeid en neem ze
  niet zonder toestemming mee in de commit.
- Als er niets is gewijzigd, is een commit niet nodig. Meld het als committen
  wordt geblokkeerd en vermeld de oorzaak.
- Vermeld na afronding kort de commit-hash en de uitgevoerde controles.
- Push alleen als de gebruiker daar opdracht toe geeft.
