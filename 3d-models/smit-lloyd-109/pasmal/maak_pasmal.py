"""Bouw de vlakke dekmal van 410 × 189 mm uit de voetafdruk van het onderdekhuis."""
from pathlib import Path
import math
import json
import sys

import cadquery as cq
import trimesh

OUTPUT = Path(__file__).resolve().parent
THICKNESS = 2.4


def box(x0, x1, y0, y1, height=THICKNESS, z=0):
    return cq.Workplane("XY").box(
        x1 - x0, y1 - y0, height, centered=(False, False, False)
    ).translate((x0, y0, z))


parameters = json.loads((OUTPUT.parent / "CAD/parameters.json").read_text())
M = parameters["measured"]
C = parameters["construction"]
A = parameters["aft"]
U = parameters["upper"]
B = parameters["bridge"]

# De omtrek komt uit dezelfde module als CAD/build.py, in v18-coördinaten:
# X=0 is de punt van de neus, Y=0 de hartlijn. Daarna schuift alles naar
# voren met de uitsteek van het grote voorblok, zodat X=0 op de mal de
# voorste punt van het voorblok is.
sys.path.insert(0, str(OUTPUT.parent / "CAD"))
import voetafdruk  # noqa: E402

S = voetafdruk.stations(parameters)
L = S["L"]
nr = S["nr"]
half_front = S["half_front"]
UX = S["UX"]
lout, yiL, rheadinner, rtaper = S["lout"], S["yiL"], S["rheadinner"], S["rtaper"]
outline = cq.Workplane("XY").polyline(voetafdruk.outline_points(parameters)).close()
template = outline.extrude(THICKNESS)


def nose_x(y):
    """X van de neuswand op dwarspositie y, zoals case_on_fore in build.py."""
    return nr - nr * math.sqrt(max(0, 1 - (y / half_front) ** 2))


# Voorblokjes als vlakke voetafdruk, met een bruggetje tot over de neuswand.
cb, sb = M["front_center_box"], M["front_small_box"]
small_y = -(cb[0] / 2 + sb[0] / 2 + C["front_small_box_gap"])
for (width, projection, _), y in [(cb, 0), (sb, small_y)]:
    front = nose_x(y) - projection
    reach = max(nose_x(y - width / 2), nose_x(y + width / 2)) + 4
    template = template.union(box(front, reach, y - width / 2, y + width / 2))

FRONT = M["front_center_box"][1]
template = template.translate((FRONT, 0, 0))
END = L + FRONT
SEAM = C["lower_split_x"] + FRONT  # zelfde naad als de onderdekhuisdelen 02/03

# Open vakken sparen materiaal; dwarsliggers rond stuurhut, naad en U-bodem.
for x0, x1, half_width in [(67, 138, 63), (155, SEAM - 10, 77),
                          (SEAM + 10, UX + FRONT - 18, 77)]:
    for y0, y1 in [(-half_width, -4), (4, half_width)]:
        template = template.cut(box(x0, x1, y0, y1, 5, -1))
# Vakken in de armen houden 6,5 mm rand, ook langs de schuine binnenkant van de uiteinden.
for y0, y1 in [(lout + 6.5, S["left_end_inner"] - 6.5), (S["right_end_inner"] + 6.5, rtaper - 6.5)]:
    template = template.cut(box(S["nt"] + FRONT + 4, L - C["end_radius"] + FRONT, y0, y1, 5, -1))

# Vier gaatjes geven de buitenhoeken van de voorlopige insteekrand aan.
frame_x0 = C["frame_center_x"] - C["frame_outer"][0] / 2 + FRONT
frame_x1 = C["frame_center_x"] + C["frame_outer"][0] / 2 + FRONT
frame_y = C["frame_outer"][1] / 2
for x in (frame_x0, frame_x1):
    for y in (-frame_y, frame_y):
        drill = cq.Workplane("XY").center(x, y).circle(1.25).extrude(5)
        template = template.cut(drill)

# Verhoogde markeringen tonen de voor- en achterrand van stuurhut en schoorsteenvoeten.
for x in (B["front_base_x"] + FRONT, B["rear_x"] + FRONT):
    template = template.union(box(x - .5, x + .5, -67, 67, .6, THICKNESS - .1))
foot = U["funnel_length"] / 2 + 2
for x in (U["funnel_center_x"] - foot + FRONT, U["funnel_center_x"] + foot + FRONT):
    for y in (U["left_funnel_y"], U["right_funnel_y"]):
        template = template.union(box(x - .5, x + .5, y - 3, y + 3, .6, THICKNESS - .1))

bounds = template.val().BoundingBox()
assert abs(bounds.xmin) < .01 and abs(bounds.xlen - END) < .01, (bounds.xmin, bounds.xlen)
assert abs(bounds.ymin - lout) < .01 and abs(bounds.ymax - S["rheadouter"]) < .01, (bounds.ymin, bounds.ymax)
print("mal", round(bounds.xlen, 2), "×", round(bounds.ylen, 2), "mm")

for number, label, x0, x1 in [(1, "voor", 0, SEAM), (2, "achter", SEAM, END)]:
    piece = template.intersect(box(x0, x1, -110, 110, 6))
    shape = piece.val()
    assert len(piece.solids().vals()) == 1 and shape.isValid(), label
    b = shape.BoundingBox()
    piece = piece.translate((-b.xmin, -b.ymin, -b.zmin))
    filename = OUTPUT / f"{number:02d}_dekmal_{label}.stl"
    cq.exporters.export(piece, str(filename), tolerance=.03, angularTolerance=.1)
    mesh = trimesh.load_mesh(filename)
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split()) == 1
    assert max(mesh.extents[:2]) <= parameters["print"]["max_footprint"]
    print(label, mesh.extents.round(2).tolist(), "mm")
