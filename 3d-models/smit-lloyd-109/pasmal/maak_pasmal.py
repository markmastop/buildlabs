"""Bouw de vlakke 380 × 200 mm pasmal uit het plaatsingsvoorstel."""
from pathlib import Path
import math

import cadquery as cq
import trimesh

OUTPUT = Path(__file__).resolve().parent
THICKNESS = 2.4


def box(x0, x1, y0, y1, height=THICKNESS, z=0):
    return cq.Workplane("XY").box(
        x1 - x0, y1 - y0, height, centered=(False, False, False)
    ).translate((x0, y0, z))


# X=0 is de punt van het grote voorblok. Y=0 is de hartlijn.
nose = [(60 - 35 * math.cos(a * math.pi / 32),
         90 * math.sin(a * math.pi / 32)) for a in range(-16, 17)]
outline = nose + [(220, 100), (380, 100), (380, 40), (265, 40),
                  (265, -40), (380, -40), (380, -100), (220, -100)]
template = cq.Workplane("XY").polyline(outline).close().extrude(THICKNESS)
# Korte bruggetjes verbinden de schematische voorblokjes met de ronde neus.
template = template.union(box(0, 29, -32.5, 32.5))
template = template.union(box(10, 37, 32.5, 57.5))

# Open vakken sparen materiaal, met dwarsliggers rond stuurhut en montagenaad.
for x0, x1, half_width in [(67, 138, 63), (155, 185, 77),
                          (195, 253, 77)]:
    for y0, y1 in [(-half_width, -4), (4, half_width)]:
        template = template.cut(box(x0, x1, y0, y1, 5, -1))
for y0, y1 in [(-92, -48), (48, 92)]:
    template = template.cut(box(302, 371, y0, y1, 5, -1))

# Vier gaatjes geven de buitenhoeken van de voorlopige insteekrand aan.
for x in (83, 287):
    for y in (-76, 76):
        drill = cq.Workplane("XY").center(x, y).circle(1.25).extrude(5)
        template = template.cut(drill)

# Verhoogde markeringen tonen de voor- en achterrand van stuurhut en voeten.
for x in (58, 148):
    template = template.union(box(x - .5, x + .5, -67, 67, .6, THICKNESS - .1))
for x in (295, 379):
    for y0, y1 in [(-99, -65), (67, 99)]:
        # Doorlopende markeringen liggen op de volle dwarsligger / eindrand.
        for a, b in [(y0, y0 + 5), (y1 - 5, y1)]:
            template = template.union(box(x - .5, x + .5, a, b, .6, THICKNESS - .1))

for number, label, x0, x1 in [(1, "voor", 0, 190), (2, "achter", 190, 380)]:
    piece = template.intersect(box(x0, x1, -105, 105, 6))
    shape = piece.val()
    assert len(piece.solids().vals()) == 1 and shape.isValid(), label
    bounds = shape.BoundingBox()
    piece = piece.translate((-bounds.xmin, -bounds.ymin, -bounds.zmin))
    filename = OUTPUT / f"{number:02d}_dekmal_{label}.stl"
    cq.exporters.export(piece, str(filename), tolerance=.03, angularTolerance=.1)
    mesh = trimesh.load_mesh(filename)
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split()) == 1
    assert max(mesh.extents) < 246
    print(label, mesh.extents.round(2).tolist(), "mm")
bounds = template.val().BoundingBox()
assert abs(bounds.xlen - 380) < .01 and abs(bounds.ylen - 200) < .01
