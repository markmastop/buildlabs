# Detailherstel p2

P1 verloor bij de CAD-omzetting te veel van de vormstudie. P2 herstelt de
zichtbare onderdelen als echte CAD- en printgeometrie. De buitenvorm en
RC-constructie blijven gebaseerd op hetzelfde model op schaal 1:100.

| Kenmerk uit vormstudie v3 | Uitwerking in de CAD-/printlijst |
|---|---|
| Relingen op dek 1, galerijdak, kompasdek, hangardak en radarplatforms | `70_reling_*`, op hun montageplek en per recht paneel printbaar |
| Vierzijdige zwarte vakwerkmast | Vier taps toelopende vlakken `32_vakwerk_*`, losse ra's en top |
| Witte radarmast met twee platforms | Dikkere mast, schuine mantel, platforms, relingen, voeten en scanners |
| Acht trappen tussen de dekken | `71_trap_*`, inclusief bomen, treden, staanders en leuningen |
| Helidek met netten, cirkel en H | Vijf roosterpanelen `72_helideknet_*`, gele cirkel en witte H als passende inleg |
| Grote oranje dubbele sloepdavits | `41_davit_*` met dwarsverbindingen en aparte hydrauliek |
| Lange knikarmkranen | `42_dekkraan_*` met voet, geknikte armen en cilinder |
| Donkere ramen in brug en accommodatie | Inzetstroken `19_*` achter de echte raamopeningen |
| Gele helikopters met cockpitramen | Zes typen gebogen inzetruit `64_heli_ruit_*`, echte uitsparingen in de romphelften |
| Hangarinterieur | Vier spanten, kasten, werkbok en rekken met de zes losse rotorbladen |
| Zodiacs en reddings-RIBs | Open kuipen, pontons, banken, spiegels, motoren en aparte davits/platforms |
| Radar-/satcomdomes, GPS, antennes, zoeklichten | `78_*` op de juiste dakposities |
| Lichtkap en banken | Witte schuine roeden en nok, echte planknaden in de zittingen |
| Schoorsteen | Donkere achterwand en drie schuine uitlaten |
| Achterste promenade en werkdek | Dichte witte/blauwe verschansing, opening voor valreep en grote dwarstank |
| Reddingsmiddelen en windsok | Vlotkokers, reddingsboeien, vlaggenstok, vlag en windsok |
| Voordek | Ankerlieren, kettingschijven, dubbele bolders, luchtkokers, bakluik en ankers |
| Rompdetails en toegang | Gesloten patrijspoortplaatjes, uitgezette valreep en gestuwde ladder |
| Scheepsnaam | Gegraveerde naamplaten op steunpootjes; geen rederijlogo's |

## Afwerking en constructie

De relingen zijn niet langer alleen generieke voorraadstroken: hun
werkelijke vorm en positie staan in de assemblage. Twee rechte stroken
blijven als reserve in de lijst. Alle inzetruiten worden ook als losse
printdelen geleverd; helder folie op basis van die vormen is een alternatief.

De rode onderzijde in de CAD-viewer toont de bedoelde schilderafwerking bij
de getekende waterlijn. De vier rompdelen zijn daar niet nogmaals gesplitst.
STL draagt geen kleuren; de losse kleuronderdelen kun je apart printen.
Naamplaten en kleine details kunnen na het printen worden geschilderd.

Relingrails zijn 1,2 mm dik en staanders 1,4 mm. De korte radarplatformrelingen hebben een volledig vlakke printzijde,
zodat ook de knierails vanaf de eerste laag op de plaat rusten. De mastvlakken
zijn 1,2 mm dik. Ruiten, vlag en patrijspoortplaatjes zijn circa 0,8–1,1 mm dik. Dit zijn
bewuste FDM-aanpassingen aan de kleinere visuele buisjes en vlakken.
Ze zijn modelbouwdetails en geen dragende of functionele RC-componenten.
Touwen, verstaging, kettingen en kabels kun je met draad toevoegen; die zijn
niet vervangen door grove kunststof staven.

De statische controle toetst onder andere de cockpitruiten tegen hun
uitsparingen, de raamstroken tegen de witte gevels, de twee helikopters tegen
de hangarinrichting en de H/cirkel tegen hun inlegvakken. Slicercontroles
staan in `../print/slicercontrole.json`. Fysieke passing en de druk-/vaartests
blijven nog uit te voeren.
