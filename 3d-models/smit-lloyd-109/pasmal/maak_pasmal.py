"""Bouw de vlakke dekmal van 410 × 189 mm uit de v17-voetafdruk."""
from pathlib import Path
import math
import json

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

# De omtrek volgt CAD/build.py stap voor stap, in v17-coördinaten:
# X=0 is de punt van de neus, Y=0 de hartlijn. Daarna schuift alles
# naar voren met de uitsteek van het grote voorblok, zodat X=0 op de mal
# de voorste punt van het voorblok is.
L = M["length"]
H = C["aft_halfwidth"]
nr = C["fore_nose_depth"]
yiL = -H + M["left_narrow"]
yiR = yiL + M["U_width"]
UX = L - M["U_depth_left"]
l3, l4 = L - M["left_F3"], L - M["left_F4"]
r3, r4 = L - M["right_F3"], L - M["right_F4"]
lout = yiL - M["left_wide"]
rib = H - M["right_bare"]
rheadinner = rib + C["right_shoulder_lateral_shift"]
rheadouter = rheadinner + M["right_wide"]
rtaper = rheadinner + M["right_bare"]
R = C["end_radius"]
nt = UX + M["U_to_low_block"]
ne = nt + C["small_notch_length"]
ny = C["small_notch_inner_y"]
n = C["fore_nose_segments"]
half_front = M["front_width"] / 2
nose = [(nr - nr * math.cos(-math.pi / 2 + i * math.pi / n),
         half_front * math.sin(-math.pi / 2 + i * math.pi / n)) for i in range(n + 1)]
outline = (
    cq.Workplane("XY").polyline(nose)
    .lineTo(M["fore_roof_length"], half_front).lineTo(UX, H).lineTo(r4, H)
    .lineTo(r3, rheadouter).lineTo(C["rear_taper_start"], rtaper)
    .lineTo(L - R, rtaper).radiusArc((L, rtaper - R), R)
    .lineTo(L, rheadinner + R).radiusArc((L - R, rheadinner), R)
    .lineTo(ne, rheadinner).lineTo(ne, ny).lineTo(nt, ny).lineTo(nt, yiR)
    .lineTo(UX + A["left_chamfer_run"], yiR).lineTo(UX, yiR - A["left_chamfer_inset"])
    .lineTo(UX, yiL + A["right_chamfer_inset"]).lineTo(UX + A["right_chamfer_run"], yiL)
    .lineTo(L - R, yiL).radiusArc((L, yiL - R), R)
    .lineTo(L, lout + R).radiusArc((L - R, lout), R)
    .lineTo(l3, lout).lineTo(l4, -H).lineTo(UX, -H)
    .lineTo(M["fore_roof_length"], -half_front).close()
)
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
for y0, y1 in [(lout + 6.5, yiL - 6.5), (rheadinner + 6.5, rtaper - 6.5)]:
    template = template.cut(box(ne + FRONT + 4, END - 6, y0, y1, 5, -1))

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
assert abs(bounds.ymin - lout) < .01 and abs(bounds.ymax - rheadouter) < .01, (bounds.ymin, bounds.ymax)
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
