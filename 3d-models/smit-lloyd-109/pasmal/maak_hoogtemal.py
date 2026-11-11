"""Vlak geprinte hoogtemal met losse voet. Afmetingen in mm."""
from pathlib import Path

import cadquery as cq
import trimesh

output = Path(__file__).resolve().parent
# De inkepingen liggen op 86 en 141 mm vanaf het echte rompdek.
outline = [(0, 0), (34, 0), (34, 84), (30, 86), (34, 88),
           (34, 139), (30, 141), (34, 143), (34, 157), (0, 157)]
gauge = cq.Workplane("XY").polyline(outline).close().extrude(3)
# Positieve tekst is vlak mee te printen zonder ondersteuning.
for value, y in [(86, 80), (141, 134), (157, 151)]:
    label = cq.Workplane("XY", origin=(14, y, 2.9)).text(
        str(value), 5, .6, combine=False
    )
    gauge = gauge.union(label)
# Open sleuf loopt tot op het bed. Daardoor staat ook de mal op het rompdek.
foot = cq.Workplane("XY").box(46, 40, 8, centered=(True, True, False))
slot = cq.Workplane("XY").box(34.5, 3.3, 10, centered=(True, True, False))
foot = foot.cut(slot)

for name, part in [("hoogtemal-stuurhut", gauge), ("hoogtemal-voet", foot)]:
    assert part.val().isValid() and len(part.solids().vals()) == 1
    bounds = part.val().BoundingBox()
    part = part.translate((-bounds.xmin, -bounds.ymin, -bounds.zmin))
    path = output / f"{name}.stl"
    cq.exporters.export(part, str(path), tolerance=.03, angularTolerance=.1)
    mesh = trimesh.load_mesh(path)
    assert mesh.is_watertight and len(mesh.split()) == 1
    assert max(mesh.extents) < 246
    if name.endswith("stuurhut"):
        assert abs(mesh.extents[1] - 157) < .01
    print(name, mesh.extents.round(2).tolist())
