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

### Ontwerp van projectpagina's

Het ontwerpvoorbeeld is de Ortelius-pagina:
[`3d-models/ortelius/index.html`](3d-models/ortelius/index.html). Alle
projectpagina's, bestellijsten en kijkpagina's volgen die huisstijl. Kopieer
bij een nieuwe pagina de opbouw en de stijl van dat voorbeeld; bedenk geen
eigen kleuren, lettertypen of knopstijlen.

- **Lettertypen:** Saira Extra Condensed (koppen en grote getallen), IBM Plex
  Sans (tekst) en IBM Plex Mono (labels, hints, kleine kopjes), via
  Google Fonts:

  ```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Saira+Extra+Condensed:wght@500;700&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
  ```

- **Kleuren:** alleen deze variabelen, met de donkere variant voor
  `prefers-color-scheme: dark` en `[data-theme="dark"]`:

  ```css
:root {
  --ice: #edf2f5; --sheet: #f8fafb; --ink: #14212c; --muted: #536472; --rule: #d3dde4;
  --hull: #b3261e; --polar: #1f6f94; --stage: #dfe8ee;
  --display: "Saira Extra Condensed", "Arial Narrow", sans-serif;
  --body: "IBM Plex Sans", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --ice: #0d1720; --sheet: #142330; --ink: #e4ecf1; --muted: #93a6b4; --rule: #263a4a;
  --hull: #e0574d; --polar: #6cb8d9; --stage: #0f1e2a; color-scheme: dark } }
:root[data-theme="dark"] {
  --ice: #0d1720; --sheet: #142330; --ink: #e4ecf1; --muted: #93a6b4; --rule: #263a4a;
  --hull: #e0574d; --polar: #6cb8d9; --stage: #0f1e2a; color-scheme: dark }
  ```

- **Indeling:** één kolom in `.wrap` (maximaal 960 px, 28 px tussenruimte,
  minimaal 16 px zijmarge). Volgorde: Build Labs-knop, `<header>` met
  `.eyebrow` (mono, hoofdletters, `--polar`), `<h1>` in Saira met één
  accentwoord in `<span>` (`--hull`) en een `.lede`. Daarna eventueel een
  `.note` met de belangrijkste links, dan het model of beeld, de `.specs`-strook
  en de secties met een `<h2>` in Saira.
- **Kijkvlak:** model of beeld in `.viewer` (achtergrond `--stage`, rand
  `--rule`, hoek 6 px) met een mono-hint onderin, bijvoorbeeld
  "slepen = draaien · scrollen = zoomen".
- **Knoppen:** pillen in `.controls` (14 px, opvulling 7 × 14 px, 8 px
  tussenruimte, achtergrond `--sheet`, rand `--rule`). Aan/uit-knoppen hebben een
  bolletje en `aria-pressed`; de actieve keuze krijgt een `--polar`-rand.
  Gebruik geen gewone selectievakjes of schakelaars in het kijkgedeelte.
- **Overige onderdelen:** `.specs` (mono-label, groot Saira-getal),
  onderdelenlijsten in `.group` met een mono-kopje in `--polar`, notities en
  panelen met `--sheet` en `--rule`, tabellen in een kaart met mono-kolomkoppen.
- **Ingebedde kijkers** (iframes en `srcdoc`) krijgen dezelfde kleuren,
  lettertypen en knoppen; zie het stijlblok `sl-paginastijl` in
  `3d-models/smit-lloyd-109/index.html`.
- Controleer een gewijzigde pagina in licht en donker en op telefoonbreedte,
  zonder horizontaal scrollen.

## Projectinformatie bijhouden

- Werk bij wijzigingen in projectstatus, versie, hoofdmaten, printbestanden of bouwafhankelijkheden de projectpagina, project-README, tabel in de hoofd-README en homepagekaart samen bij.
- Gebruik op homepagekaarten dezelfde volgorde: status, schaal of hoofdmaat en beschikbare bestanden of, bij een concept, de belangrijkste ontwerpmaat of indeling. Vermeld in de omschrijving wat de maat betreft, zoals de romp, bovenbouw of voet.
- Baseer status en bestandsformaten op de actuele projectdocumentatie en bestanden in Git. Maak onderscheid tussen een concept, beschikbare printset of printprototype, digitale controles en fysiek bevestigde passing of werking. Tel alleen bestanden van de vermelde versie en geef aan of pasproefbestanden meetellen.
- Vermeld benodigde bestaande onderdelen, zoals een RC-romp of chassis, inclusief de relevante aansluitmaat. Als een project meerdere uitvoeringen heeft, geef per uitvoering aan wat nodig is.
- Link bij een printset waar mogelijk rechtstreeks naar de printbestanden of de handleiding die ze ontsluit.

### Versienummers

- Elk project heeft één doorlopende versiereeks: `v1`, `v2`, `v3` … In lopende
  tekst mag ook "versie 18". Gebruik geen andere voorvoegsels (zoals `p1` of
  `r2`) en geen aparte reeksen voor concept, CAD, print of deelmodules: een
  nieuw stadium telt gewoon door. Voorbeeld Ortelius: v1–v3 vormstudie, v4 en
  v5 CAD- en printprototype, v6 aandrijving.
- Verhoog het nummer wanneer geometrie of printbestanden veranderen ten
  opzichte van de laatst gepubliceerde (gepushte) versie. Tekst, opmaak en
  documentatie veranderen het nummer niet.
- Gebruik hetzelfde nummer in bestandsnamen (`SL109_v18_assemblage.step`,
  `ortelius-v5-assemblage.step`), op de projectpagina, in beide README's en op
  de homepagekaart. Bestaat een deel uit een eerdere versie, noem dat erbij
  ("romp en opbouw v5, aandrijving v6").
- Hernoem je een oude reeks, vermeld de oude namen één keer in de
  project-README, zodat oude verwijzingen te volgen blijven.

### Bevestigde eindstatussen

De eigenaar heeft de volgende ontwerpen als Final bevestigd. Gebruik deze
status op de homepagekaart, de projectpagina en in beide README’s. Leg
digitale controles en fysieke passing vast op basis van de projectdocumentatie.

- Dashboard: dubbele voorspeakers: **Final v7**.
- Dashboard: subwoofer: **Final v2.5.1**.
- EnergyDeck 7-inch behuizing: **Final v9**.
- EnergyDeck 5-inch behuizing: **Final**.
- Zes geometrische workshopmodellen: **Final**.
- Truma Therme-montageplaat: **Final v17**.

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
