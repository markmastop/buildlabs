"""Teken de maataanzichten (boven- en zijaanzicht) uit de assemblage-STEP.

Gebruik vanuit de projectmap: python CAD/maataanzichten.py
Orthografische projectie, 2 px per mm. Driehoeken en zichtbare kanten worden
samen op diepte gesorteerd (schildersalgoritme), zodat achterliggende kanten
grotendeels wegvallen. Vereist CadQuery en trimesh, net als build.py.
"""
from pathlib import Path
import json
import sys

import cadquery as cq
import numpy as np
import trimesh

R = Path(__file__).resolve().parents[1]
P = json.loads((R / 'CAD/parameters.json').read_text())
VERSION = P['version']
SCALE = 2.0
FEATURE_ANGLE = np.radians(25)
STYLE = ('text{font-family:Arial,sans-serif;fill:#173042}.dim{stroke:#b22b30;stroke-width:2;fill:none}'
         '.edge{stroke:#526775;stroke-width:.8;fill:none;stroke-linecap:round}'
         '.f{fill:#e2e9ed;stroke:#e2e9ed;stroke-width:.35;stroke-linejoin:round}')


def load_parts(names=None):
    controle = json.loads((R / 'controle.json').read_text())
    assembled = [p['part'] for p in controle['parts'] if p['assembled']]
    solids = cq.importers.importStep(str(R / f'STEP/SL109_{VERSION}_assemblage.step')).solids().vals()
    assert len(solids) == len(assembled)
    meshes = []
    for name, solid in zip(assembled, solids):
        if names and not any(name.startswith(n) for n in names):
            continue
        vertices, triangles = solid.tessellate(.05, .2)
        mesh = trimesh.Trimesh([(v.x, v.y, v.z) for v in vertices], triangles, process=True)
        meshes.append(mesh)
    return meshes


def project(meshes, toward_viewer, to_2d):
    """Lijst van (diepte, soort, 2D-punten) voor zichtbare driehoeken en kanten."""
    items = []
    view = np.asarray(toward_viewer, float)
    for mesh in meshes:
        depth = mesh.vertices @ view
        facing = mesh.face_normals @ view > 1e-6
        for face in np.nonzero(facing)[0]:
            idx = mesh.faces[face]
            items.append((depth[idx].mean(), 0, to_2d(mesh.vertices[idx])))
        # Feature edges: boundary of the visible region or a crease above the angle limit.
        adj = mesh.face_adjacency
        crease = mesh.face_adjacency_angles > FEATURE_ANGLE
        silhouette = facing[adj[:, 0]] != facing[adj[:, 1]]
        visible = facing[adj[:, 0]] | facing[adj[:, 1]]
        for edge in mesh.face_adjacency_edges[(crease | silhouette) & visible]:
            items.append((depth[edge].max() + .02, 1, to_2d(mesh.vertices[edge])))
    items.sort(key=lambda item: (item[0], item[1]))
    return items


def svg_body(items):
    out = []
    edges = []

    def flush():
        if edges:
            out.append('<path class="edge" d="' + ''.join(edges) + '"/>')
            edges.clear()
    for _, kind, pts in items:
        if kind == 0:
            flush()
            out.append('<polygon class="f" points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts) + '"/>')
        else:
            (x0, y0), (x1, y1) = pts
            edges.append(f'M{x0:.2f},{y0:.2f}L{x1:.2f},{y1:.2f}')
    flush()
    return out


def dimension(x0, y0, x1, y1):
    return (f'<path class="dim" d="M{x0},{y0} L{x1},{y1} M{x0 - 6},{y0 - 6} l12,12 '
            f'M{x1 - 6},{y1 - 6} l12,12"/>')


def fmt(value):
    return f'{value:.0f}' if abs(value - round(value)) < .05 else f'{value:.1f}'.replace('.', ',')


def drawing(title, body, extra, footer):
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 760">',
            '<rect width="1120" height="760" fill="white"/>', f'<style>{STYLE}</style>',
            f'<text x="50" y="45" font-size="28">Smit-Lloyd 109 · {title}</text>',
            f'<text x="50" y="78" font-size="18">{VERSION.upper()} · alle maten in mm · voorzijde links · geen afdruk op schaal</text>']
    tail = [f'<text x="50" y="680" font-size="22">{footer[0]}</text>',
            f'<text x="50" y="715" font-size="18">{footer[1]}</text>', '</svg>']
    return '\n'.join(head + body + extra + tail) + '\n'


def main():
    meshes = load_parts()
    allv = np.vstack([m.vertices for m in meshes])
    xmin, ymin, zmin = allv.min(0)
    xmax, ymax, zmax = allv.max(0)
    x0 = 75 - SCALE * xmin
    C = P['construction']
    opening = C['opening']
    frame = C['frame_outer']

    # Top view: front left, export +Y up (a proper view from above).
    yc = 360
    top = project(meshes, (0, 0, 1), lambda v: np.c_[x0 + SCALE * v[:, 0], yc - SCALE * v[:, 1]])
    ytop, ybot = yc - SCALE * ymax, yc - SCALE * ymin
    xl, xr = x0 + SCALE * xmin, x0 + SCALE * xmax
    extra = [dimension(round(xl), 625, round(xr), 625),
             f'<text x="{(xl + xr) / 2 - 78:.1f}" y="613.0" font-size="24">{fmt(xmax - xmin)} totaal</text>',
             dimension(945, round(ytop), 945, round(ybot)),
             f'<text x="957.0" y="{(ytop + ybot) / 2 - 6:.1f}" font-size="24">{fmt(ymax - ymin)} max.</text>']
    footer = (f'Rompopening {opening[0]} × {opening[1]} · insteekrand {frame[0]} × {frame[1]}',
              'Nominale speling 0,5 per zijde · positie pasframe nog te bepalen op de romp.')
    (R / f'beelden/bovenaanzicht-maten-{VERSION}.svg').write_text(drawing('bovenaanzicht', svg_body(top), extra, footer))

    # Side view from side A (export -Y), front left, deck Z=0 on the blue line.
    zdeck = 550
    side = project(meshes, (0, -1, 0), lambda v: np.c_[x0 + SCALE * v[:, 0], zdeck - SCALE * v[:, 2]])
    zt = zdeck - SCALE * zmax
    insert = -zmin
    extra = [dimension(round(xl), 625, round(xr), 625),
             f'<text x="{(xl + xr) / 2 - 78:.1f}" y="613.0" font-size="24">{fmt(xmax - xmin)} totaal</text>',
             dimension(945, round(zt), 945, zdeck),
             f'<text x="957.0" y="{(zt + zdeck) / 2 - 12:.1f}" font-size="24">{fmt(zmax)}</text>',
             f'<path d="M65,{zdeck}H910" stroke="#176c94" stroke-dasharray="8 5"/>']
    footer = (f'Hoogte boven rompdek {fmt(zmax)} · inclusief insteekrand {fmt(zmax - zmin)}',
              f'Blauwe lijn: rompdek Z=0 · insteekdiepte {fmt(insert)} onder dek · zonder mast.')
    (R / f'beelden/zijaanzicht-maten-{VERSION}.svg').write_text(drawing('zijaanzicht', svg_body(side), extra, footer))
    print('maataanzichten', VERSION, fmt(xmax - xmin), fmt(ymax - ymin), fmt(zmax))


def check_view(out, names, toward_viewer, axes):
    """Losse controleweergave van enkele delen, bijvoorbeeld een schoorsteen."""
    meshes = load_parts(names)
    allv = np.vstack([m.vertices for m in meshes])
    a, b = axes
    sx, sy = (1 if a >= 0 else -1), (1 if b >= 0 else -1)
    ia, ib = abs(a) - 1, abs(b) - 1
    lo = np.array([min(sx * allv[:, ia]), min(sy * allv[:, ib])])
    to_2d = lambda v: np.c_[20 + 6 * (sx * v[:, ia] - lo[0]), 1180 - 6 * (sy * v[:, ib] - lo[1])]
    body = svg_body(project(meshes, toward_viewer, to_2d))
    Path(out).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200">'
                         f'<rect width="1200" height="1200" fill="white"/><style>{STYLE}</style>'
                         + '\n'.join(body) + '</svg>\n')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'controle':
        # python CAD/maataanzichten.py controle uit.svg 15_schoorsteen_logo_roosters_L vx,vy,vz as1,as2
        check_view(sys.argv[2], sys.argv[3].split(','), [float(v) for v in sys.argv[4].split(',')],
                   [int(v) for v in sys.argv[5].split(',')])
    else:
        main()
