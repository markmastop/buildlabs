"""Bouw de vlakke 380 × 200 mm pasmal uit het plaatsingsvoorstel."""
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


# X=0 is de punt van het grote voorblok. Y=0 is de hartlijn.
parameters = json.loads((OUTPUT.parent / "CAD/parameters.json").read_text())
measured = parameters["measured"]
construction = parameters["construction"]
aft = parameters["aft"]
# Behoud de gemeten asymmetrie en knikken van de v17-uitsparing.
# De achterste stations schuiven 30 mm naar voren.
end = 380
half_width = construction["aft_halfwidth"]
left_inner = -half_width + measured["left_narrow"]
right_inner = left_inner + measured["U_width"]
notch_start = end - measured["U_depth_left"]
step_start = notch_start + measured["U_to_low_block"]
step_end = step_start + construction["small_notch_length"]
step_y = construction["small_notch_inner_y"]
right_shoulder = half_width - measured["right_bare"] + construction["right_shoulder_lateral_shift"]
left_outer = left_inner - measured["left_wide"] - 5.5
right_outer = right_shoulder + measured["right_wide"] + 5.5
right_end = right_shoulder + measured["right_bare"] + 5.5
radius = construction["end_radius"]
nose = [(60 - 35 * math.cos(a * math.pi / 96),
         90 * math.sin(a * math.pi / 96)) for a in range(-48, 49)]
outline = (
    cq.Workplane("XY").polyline(nose)
    .lineTo(188, 90).lineTo(notch_start, half_width)
    .lineTo(end - measured["right_F4"], half_width)
    .lineTo(end - measured["right_F3"], right_outer)
    .lineTo(construction["rear_taper_start"] - 5, right_end)
    .lineTo(end - radius, right_end).radiusArc((end, right_end - radius), radius)
    .lineTo(end, right_shoulder + radius).radiusArc((end - radius, right_shoulder), radius)
    .lineTo(step_end, right_shoulder).lineTo(step_end, step_y)
    .lineTo(step_start, step_y).lineTo(step_start, right_inner)
    .lineTo(notch_start + aft["left_chamfer_run"], right_inner)
    .lineTo(notch_start, right_inner - aft["left_chamfer_inset"])
    .lineTo(notch_start, left_inner + aft["right_chamfer_inset"])
    .lineTo(notch_start + aft["right_chamfer_run"], left_inner)
    .lineTo(end - radius, left_inner).radiusArc((end, left_inner - radius), radius)
    .lineTo(end, left_outer + radius).radiusArc((end - radius, left_outer), radius)
    .lineTo(end - measured["left_F3"], left_outer)
    .lineTo(end - measured["left_F4"], -half_width)
    .lineTo(notch_start, -half_width).lineTo(188, -90).close()
)
template = outline.extrude(THICKNESS)
# Korte bruggetjes verbinden de schematische voorblokjes met de ronde neus.
template = template.union(box(0, 29, -32.5, 32.5))
template = template.union(box(10, 37, 32.5, 57.5))

# Open vakken sparen materiaal, met dwarsliggers rond stuurhut en montagenaad.
for x0, x1, half_width in [(67, 138, 63), (155, 185, 77),
                          (195, 253, 77)]:
    for y0, y1 in [(-half_width, -4), (4, half_width)]:
        template = template.cut(box(x0, x1, y0, y1, 5, -1))
for y0, y1 in [(-91, -69), (66, 87)]:
    template = template.cut(box(309, 369, y0, y1, 5, -1))

# Vier gaatjes geven de buitenhoeken van de voorlopige insteekrand aan.
for x in (83, 287):
    for y in (-76, 76):
        drill = cq.Workplane("XY").center(x, y).circle(1.25).extrude(5)
        template = template.cut(drill)

# Verhoogde markeringen tonen de voor- en achterrand van stuurhut en voeten.
for x in (58, 148):
    template = template.union(box(x - .5, x + .5, -67, 67, .6, THICKNESS - .1))
for x in (295, 379):
    for y in (-82, 76):
        template = template.union(box(x - .5, x + .5, y - 3, y + 3, .6, THICKNESS - .1))

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
