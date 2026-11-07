# Werkafspraken voor agents

Deze afspraken gelden voor de hele repository.

## Structuur

- Elk project staat in een eigen map binnen de juiste categorie, bijvoorbeeld
  `3d-models/<projectnaam>/`. Gebruik kleine letters en koppeltekens voor
  mapnamen.
- Elk project heeft een `README.md` met: wat het is, de status, belangrijkste
  maten of keuzes, de bestanden en de volgende stappen.
- Voeg een nieuw project ook toe aan de tabel in de hoofd-`README.md` en als
  kaart aan de startpagina `index.html` in de root (GitHub Pages).
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

## Projectpagina's (GitHub Pages)

- Elk project met een model heeft een `index.html` in de projectmap. Link op
  de startpagina en in de README's altijd expliciet naar `.../index.html`.
- Elke projectpagina begint met de **Build Labs-knop** terug naar de
  startpagina: direct na `<body>` (binnen de buitenste wrapper), vóór de
  `<header>`. Gebruik exact deze code, zodat de knop overal gelijk is en het
  licht- en donkerthema van de pagina volgt:

  CSS, in de `<head>`:

  ```html
<style>.bl-home{justify-self:start;align-self:start;display:inline-flex;align-items:center;gap:8px;width:max-content;margin:0 0 4px;padding:7px 14px 7px 11px;border:1px solid rgba(127,140,150,.45);border-radius:999px;font:500 14px/1 "IBM Plex Sans",system-ui,sans-serif;color:inherit;text-decoration:none;background:transparent;transition:border-color .15s,background .15s}.bl-home:hover{border-color:currentColor;background:rgba(127,140,150,.12)}.bl-home:focus-visible{outline:2px solid currentColor;outline-offset:2px}.bl-home svg{width:15px;height:15px;flex:none}</style>
  ```

  HTML:

  ```html
<a class="bl-home" href="../../index.html" aria-label="Terug naar het Build Labs-overzicht"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/><path d="M10 19.5v-5h4v5"/></svg>Build Labs</a>
  ```

- Pas `href` alleen aan als de pagina dieper ligt dan `3d-models/<project>/`.
- Gebruik geen andere terugkoppelingen (zoals losse tekstlinks) naast deze knop.
- Een projectpagina is een volledig HTML-document: `<!doctype html>`,
  `<meta charset="utf-8">` en een viewport-meta.

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
