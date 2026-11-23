"""Werk de ingebedde 3D-kijkmodellen bij uit de assemblage-STEP.

Gebruik vanuit de projectmap, na build.py: python CAD/kijkmodel.py
Bijgewerkt worden kaart.html (homepagekaart), bekijken.html en het ingebedde
kijkmodel in index.html. Ze delen één geometrieblok met twee varianten: de
actuele versie en de vorige versie ter vergelijking. Ongewijzigde onderdelen
houden hun bestaande meshdata; de vorige versie verwijst daar dan naar.

Viewercoördinaten: X - L/2, Y = export-Y, Z - 95 mm (rompdek op Z=-95).
"""
from pathlib import Path
import base64
import gzip
import html
import json
import re

import cadquery as cq
import numpy as np

R = Path(__file__).resolve().parents[1]
P = json.loads((R / 'CAD/parameters.json').read_text())
VERSION = P['version']
OFFSET = np.array([-P['measured']['length'] / 2, 0, -95.0])
BLOB = re.compile(r'(<script type="application/json" class="sl-geometry">)(.*?)(</script>)', re.S)


def decode(part):
    v = np.frombuffer(base64.b64decode(part['v16']), dtype='<i2').reshape(-1, 3) / 100
    key = 'f32' if 'f32' in part else 'f16'
    f = np.frombuffer(base64.b64decode(part[key]), dtype='<u4' if key == 'f32' else '<u2').reshape(-1, 3)
    return v, f


def volume(v, f):
    a, b, c = v[f[:, 0]], v[f[:, 1]], v[f[:, 2]]
    return float(np.einsum('ij,ij->i', a, np.cross(b, c)).sum() / 6)


def encode(name, solid, roof, base):
    vertices, triangles = solid.tessellate(.05, .3)
    v = np.array([(p.x, p.y, p.z) for p in vertices]) + OFFSET
    q = np.round(v * 100)
    assert np.abs(q).max() < 32767, name
    f = np.array(triangles, dtype=np.uint32)
    part = dict(name=name, roof=roof, base=base, v16=base64.b64encode(q.astype('<i2').tobytes()).decode())
    if len(v) < 65536:
        part['f16'] = base64.b64encode(f.astype('<u2').tobytes()).decode()
    else:
        part['f32'] = base64.b64encode(f.astype('<u4').tobytes()).decode()
    return part


def same_geometry(old, solid):
    v, f = decode(old)
    bb = solid.BoundingBox()
    lo = np.array([bb.xmin, bb.ymin, bb.zmin]) + OFFSET
    hi = np.array([bb.xmax, bb.ymax, bb.zmax]) + OFFSET
    if np.abs(v.min(0) - lo).max() > .03 or np.abs(v.max(0) - hi).max() > .03:
        return False
    return abs(volume(v, f) - solid.Volume()) <= .003 * solid.Volume() + 1


def build_variants(old_variants):
    first = next(iter(old_variants))
    resolved = {first: old_variants[first]}
    for key in old_variants:
        if key != first:
            resolved[key] = [old_variants[first][p['ref']] if 'ref' in p else p for p in old_variants[key]]
    # Opnieuw draaien binnen dezelfde versie: vergelijk dan met de versie daarvoor.
    previous = first if first != VERSION else next(k for k in old_variants if k != VERSION)
    # Bestaande meshdata per naam, uit alle varianten (de actuele eerst).
    pool = {}
    for key in [first] + [k for k in resolved if k != first]:
        for p in resolved[key]:
            pool.setdefault(p['name'], []).append(p)
    prev_parts = {p['name']: p for p in resolved[previous]}
    controle = json.loads((R / 'controle.json').read_text())
    assembled = [p for p in controle['parts'] if p['assembled']]
    solids = cq.importers.importStep(str(R / f'STEP/SL109_{VERSION}_assemblage.step')).solids().vals()
    assert len(solids) == len(assembled)
    current, reused, changed = [], {}, []
    for record, solid in zip(assembled, solids):
        name = record['part']
        old = next((p for p in pool.get(name, []) if same_geometry(p, solid)), None)
        if old is not None:
            reused[id(old)] = len(current)
            current.append(old)
            if old is not prev_parts.get(name):
                changed.append(name)
        else:
            changed.append(name)
            part = encode(name, solid, record['roof'], record['measured_base'])
            old = prev_parts.get(name)
            if old is not None and 'logoEdges' in old:
                # Het logo-reliëf zelf is ongewijzigd: de lijntekening blijft geldig.
                part = dict(list(part.items())[:3] + [('logoEdges', old['logoEdges'])] + list(part.items())[3:])
            current.append(part)
    before = [dict(ref=reused[id(p)]) if id(p) in reused else p for p in resolved[previous]]
    print('kijkmodel', VERSION, 'tegenover', previous, '· nieuw of gewijzigd:', ', '.join(changed),
          '· vervallen:', ', '.join(n for n in prev_parts if n not in {r['part'] for r in assembled}) or '-')
    return previous, {VERSION: current, previous: before}


# Teksten in de viewer die per versie meeschuiven. Een tekst moet aanwezig zijn, oud of al
# bijgewerkt (bij opnieuw draaien binnen dezelfde versie).
def texts(previous):
    assert (previous, VERSION) == ('v17', 'v18'), 'werk de viewerteksten bij voor deze versiestap'
    return [
        ("variants.v16=variants.v16.map(p=>('ref' in p)?variants.v17[p.ref]:p);",
         "variants.v17=variants.v17.map(p=>('ref' in p)?variants.v18[p.ref]:p);"),
        ('data-variant="v17" aria-pressed="true">V17</button>', 'data-variant="v18" aria-pressed="true">V18</button>'),
        ('data-variant="v16" aria-pressed="false">Vergelijk v16</button>', 'data-variant="v17" aria-pressed="false">Vergelijk v17</button>'),
        (re.compile(r"'Vorige versie v1[67] · [^']*'"),
         "'Vorige versie v17 · schuine U-hoeken met deur, armuiteinden R5'"),
        (re.compile(r"'V1[67] · [^']*'"),
         "'V17 · schuine U-hoeken, deur in de hoek · hoeken R2/R5'"),
        (re.compile(r"'(?:Stuurhutwand 55 mm · voet 90 mm|Onderdekhuis volgt de echte opbouw[^·']*) · voorbeeldromp uitsluitend visueel, niet opgemeten'"),
         "'Onderdekhuis volgt de echte opbouw, met trap, kasten en deur · voorbeeldromp uitsluitend visueel, niet opgemeten'"),
        ("variant='v17'", "variant='v18'"),
        ("variant==='v17'", "variant==='v18'"),
        ('Volledige opbouw v17', 'Volledige opbouw v18'),
        ('Smit-Lloyd 109 volledig model v17', 'Smit-Lloyd 109 volledig model v18'),
        ('Smit Lloyd 109 Volledig V17', 'Smit Lloyd 109 Volledig V18'),
        ('sl109-volledig-v17', 'sl109-volledig-v18'),
        (re.compile(r'aria-label="Volledige draaibare opbouw v1[78]\.[^"]*"'),
         'aria-label="Volledige draaibare opbouw v18. Het onderdekhuis volgt de echte opbouw: vlak blok aan '
         'de brede arm, rechte U-bodem, armuiteinden die binnen schuin naar buiten lopen, armuiteinden R8 en '
         'voorblokken R6. Trap met getrapte kast, twee achterkasten en de deur met patrijspoort staan erop. '
         'De schoorstenen zijn achteraan binnen versmald langs de armrand. '
         'Stuurhutwand 55 mm hoog, voetlengte 90 mm, breedte 136 mm. Vergelijk met v17. Stuurhutmaten en '
         'detailvormen zijn proefmaten uit fotoverhoudingen."'),
    ]


def update_source(src, blob, previous):
    m = BLOB.search(src)
    assert m, 'geen geometrieblok'
    body = src[:m.start(2)] + '\0BLOB\0' + src[m.end(2):]
    for old, new in texts(previous):
        if isinstance(old, re.Pattern):
            body, n = old.subn(new, body)
        else:
            n = body.count(old) or body.count(new)
            body = body.replace(old, new)
        assert n >= 1, ('tekst niet gevonden', str(old)[:60])
    rest = body.replace('p.v16', '')
    assert 'v16' not in rest and 'V16' not in rest, 'oude versie in tekst'
    return body.replace('\0BLOB\0', blob)


def main():
    kaart = (R / 'kaart.html').read_text()
    old = json.loads(gzip.decompress(base64.b64decode(json.loads(BLOB.search(kaart).group(2))['gzip'])))
    previous, variants = build_variants(old)
    packed = gzip.compress(json.dumps(variants, separators=(',', ':')).encode(), 9, mtime=0)
    blob = json.dumps({'gzip': base64.b64encode(packed).decode()})
    (R / 'kaart.html').write_text(update_source(kaart, blob, previous))
    for name, attr in [('bekijken.html', 'data-srcdoc'), ('index.html', 'srcdoc')]:
        page = (R / name).read_text()
        m = re.search(attr + r'="(.*?)"', page, re.S)
        src = update_source(html.unescape(m.group(1)), blob, previous)
        page = page[:m.start(1)] + html.escape(src, quote=True) + page[m.end(1):]
        (R / name).write_text(page)
    print('bijgewerkt: kaart.html, bekijken.html, index.html ·', len(blob), 'tekens geometrie')


if __name__ == '__main__':
    main()
