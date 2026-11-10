"""Genereer de verstelbare Ortelius-motorsteun, Fusion-assemblage en pasdelen."""
import json
import math
from pathlib import Path

import cadquery as cq
import trimesh

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
P = json.loads((HERE / 'maten.json').read_text())
MANIFEST = json.loads((PROJECT / 'print/onderdelen.json').read_text())
PARTS = {part['name']: part for part in MANIFEST['parts']}
PROP = json.loads((PROJECT / 'cad/parameters.json').read_text())['stern']['propeller']
AXIS_ORIGIN = (PROP['hub_x'], 0, PROP['hub_z'])
ANGLE = math.degrees(math.atan(PROP['shaft_slope']))

# Lokale coördinaten: u naar de motor langs de schroefas, y naar bakboord,
# w loodrecht boven de as. De oorsprong is het midden van de schroefnaaf.
def in_ship(shape):
    return shape.rotate((0, 0, 0), (0, 1, 0), -ANGLE).translate(AXIS_ORIGIN)


def on_axis(start, length, diameter, y=0, w=0):
    return cq.Solid.makeCylinder(
        diameter / 2, length, cq.Vector(start, y, w), cq.Vector(1, 0, 0)
    )


def block(u0, u1, y0, y1, w0, w1):
    return cq.Solid.makeBox(u1-u0, y1-y0, w1-w0, cq.Vector(u0, y0, w0))


def upright(u, y, w, diameter, height):
    return cq.Solid.makeCylinder(diameter / 2, height, cq.Vector(u, y, w))


def ship_part(name):
    record = PARTS[name]
    shape = cq.importers.importStep(str(PROJECT / 'cad/step' / f'{name}.step')).val()
    shape = shape.translate(tuple(-v for v in record['bed_translation']))
    if record['rotation']:
        axis, angle = record['rotation']
        shape = shape.rotate((0, 0, 0), axis, -angle)
    return shape


def normalize_step(path):
    # OCCT voegt spaties toe na de STEP-regels.
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')


def export_part(name, shape):
    assert shape.isValid() and len(shape.Solids()) == 1, name
    bounds = shape.BoundingBox()
    shape = shape.translate((-bounds.xmin, -bounds.ymin, -bounds.zmin))
    step = HERE / f'{name}.step'
    cq.exporters.export(shape, str(step))
    normalize_step(step)
    stl = HERE / f'{name}.stl'
    cq.exporters.export(shape, str(stl), tolerance=.025, angularTolerance=.10)
    mesh = trimesh.load_mesh(stl, process=True)
    assert mesh.is_watertight and mesh.is_winding_consistent, name
    assert len(mesh.split()) == 1 and max(mesh.extents) < 246, name
    assert abs(mesh.volume - shape.Volume()) / shape.Volume() < .015, name


def main():
    motor = P['motor']
    tube = P['stevenbuis']
    sleeve = P['doorvoerbus']
    coupling = P['koppeling']
    prop = P['schroef']
    mount = P['steun']
    hub_start = prop['naafcentrum_u'] - prop['naaflengte'] / 2
    hub_end = hub_start + prop['naaflengte']

    shaft_start = P['schroefas']['begin_u']
    shaft_end = shaft_start + P['schroefas']['lengte']
    tube_end = tube['begin_u'] + tube['lengte']
    coupling_start = shaft_end - coupling['insteek_as']
    coupling_end = coupling_start + coupling['lengte']
    face = coupling_end + coupling['afstand_motorvlak']
    face_thickness = mount['flensdikte']
    base_z = -mount['as_boven_voet']
    base_top = base_z + mount['bodemdikte']
    slot_centres = [face + offset for offset in mount['boutposities_vanaf_motorvlak']]
    rail_y = mount['halve_railafstand']
    rail_half_width = mount['railbreedte'] / 2
    slot_travel = mount['slag_per_richting']

    aft_hull = ship_part('01_romp_1')
    motor_hull = ship_part('01_romp_2')
    hull_joint = ship_part('02_lasstrook_1')
    rudder = ship_part('56_roerblad')
    rear_deck = ship_part('03_werkdek_achter')
    half_width = rail_y + rail_half_width + 1

    base = block(face-face_thickness, face+motor['lengte']+5, -half_width, half_width, base_z, base_top)
    flange = block(face-face_thickness, face, -20, 20, base_top-1, 15)
    # U-vorm houdt de koppeling vrij en maakt toegang van boven mogelijk.
    clearance = on_axis(face-face_thickness-1, face_thickness+2, mount['vrije_diameter_flens'])
    opening_half = mount['vrije_diameter_flens'] / 2
    flange = flange.cut(clearance).cut(
        block(face-face_thickness-1, face+1, -opening_half, opening_half, 0, 16)
    )
    for side in (-1, 1):
        flange = flange.cut(on_axis(
            face-face_thickness-1, face_thickness+2, 3.4, side*motor['bouthartafstand']/2
        ))

    # Schoren aan de koppelingzijde laten ruimte voor het motorhuis en de ventilatie.
    bracket = base.fuse(flange)
    for side in (-1, 1):
        brace = cq.Workplane('XZ', origin=(0, side*17+1.5, 0)).polyline([
            (face-face_thickness-11, base_top-1),
            (face-face_thickness+0.5, base_top-1),
            (face-face_thickness+0.5, 1),
        ]).close().extrude(3).val()
        # De voet loopt lokaal door onder de voorste schoren.
        tab = block(face-face_thickness-11, face-face_thickness+1,
                    side*17-1.5, side*17+1.5, base_z, base_top)
        bracket = bracket.fuse(tab, brace)
    for u in slot_centres:
        for y in (-rail_y, rail_y):
            slot = block(u-slot_travel, u+slot_travel, y-1.7, y+1.7, base_z-1, base_top+1)
            for end in (u-slot_travel, u+slot_travel):
                slot = slot.fuse(upright(end, y, base_z-1, 3.4, mount['bodemdikte']+2))
            bracket = bracket.cut(slot)
    bracket = bracket.clean()

    rails = []
    rail_length = (slot_centres[0]-8, slot_centres[-1]+8)
    glue_gap = mount['lijmspleet']
    for y in (-rail_y, rail_y):
        rail = block(*rail_length, y-rail_half_width, y+rail_half_width, base_z-30, base_z)
        for u in slot_centres:
            rail = rail.cut(upright(
                u, y, base_z-mount['inzetdiepte'], mount['inzetboring'], mount['inzetdiepte']+1
            ))
        # De hoogste component volgt de werkelijke binnenhuid van rompdeel 2.
        fitted = in_ship(rail).cut(motor_hull.translate((0, 0, glue_gap)))
        fitted = max(fitted.Solids(), key=lambda solid: solid.Center().z).clean()
        fitted_local = fitted.translate(tuple(-v for v in AXIS_ORIGIN)).rotate(
            (0, 0, 0), (0, 1, 0), ANGLE
        )
        rails.append((fitted, fitted_local))

    aligner = on_axis(0, coupling['lengte'], 12).cut(
        on_axis(-1, coupling['insteek_as']+1.5, 4.2)
    ).cut(
        on_axis(coupling['lengte']-motor['aslengte']+coupling['afstand_motorvlak']-.5,
                motor['aslengte']+1, 3.35)
    )
    # Print de steun met vlakke voet en de lijmvoeten op hun bovenvlak.
    export_part('motorsteun', bracket)
    for label, (_, local) in zip(('stuurboord', 'bakboord'), rails):
        export_part(f'lijmvoet-{label}', local.rotate((0, 0, 0), (1, 0, 0), 180))
    export_part('uitlijnmal', aligner.rotate((0, 0, 0), (0, 1, 0), -90))

    motor_body = in_ship(on_axis(face, motor['lengte'], motor['diameter']))
    motor_shaft = in_ship(on_axis(face-motor['aslengte'], motor['aslengte'], motor['asdiameter']))
    coupling_ref = in_ship(on_axis(coupling_start, coupling['lengte'], coupling['diameter'])
                           .cut(on_axis(coupling_start-.1, coupling['insteek_as']+.2, 4.02))
                           .cut(on_axis(face-motor['aslengte']-.1, motor['aslengte']+.2, 3.19)))
    shaft_ref = in_ship(on_axis(shaft_start, P['schroefas']['lengte'], 4))
    tube_ref = in_ship(on_axis(tube['begin_u'], tube['lengte'], tube['diameter'])
                       .fuse(on_axis(tube_end-tube['lagerlengte'], tube['lagerlengte'], tube['lagerdiameter']))
                       .cut(on_axis(tube['begin_u']-1, tube['lengte']+2, 4.1)))
    sleeve_ref = in_ship(on_axis(sleeve['begin_u'], sleeve['lengte'], sleeve['diameter'])
                         .cut(on_axis(sleeve['begin_u']-1, sleeve['lengte']+2, sleeve['boring']))
                         .cut(on_axis(sleeve['begin_u']-1, sleeve['verzinkdiepte']+1, sleeve['verzinkdiameter'])))
    hub = in_ship(on_axis(hub_start, prop['naaflengte'], prop['naafdiameter'])
                  .cut(on_axis(shaft_start, hub_end-shaft_start+1, 4.02)))
    nut = in_ship(on_axis(hub_end, P['schroefas']['borgmoer_ruimte'], 8)
                  .cut(on_axis(hub_end-1, P['schroefas']['borgmoer_ruimte']+2, 4.02)))
    depth = prop['voorlopige_bladzone']
    sweep = in_ship(on_axis(-depth/2, depth, prop['diameter']).cut(
        on_axis(-depth/2-1, depth+2, prop['naafdiameter'])
    ))
    bracket_world = in_ship(bracket)

    nut_end = hub_end + P['schroefas']['borgmoer_ruimte']
    assert hub_start <= shaft_start < hub_end
    assert shaft_start + P['schroefas']['draadlengte'] >= nut_end
    assert tube['begin_u'] > nut_end
    assert coupling_start > tube_end and face-motor['aslengte'] > shaft_end
    assert all(s.isValid() for s in (motor_body, coupling_ref, shaft_ref, tube_ref, sweep))
    for name, part in [('motor', motor_body), ('koppeling', coupling_ref),
                       ('motorsteun', bracket_world), ('motoras', motor_shaft)]:
        for obstacle in (aft_hull, motor_hull, hull_joint, rear_deck):
            assert part.intersect(obstacle).Volume() < .02, (name, 'romp of dek')
    for shift in (-slot_travel, 0, slot_travel):
        moved = in_ship(bracket.translate((shift, 0, 0)))
        for y, (foot, _) in zip((-rail_y, rail_y), rails):
            assert moved.intersect(foot).Volume() < .02, 'motorsteun tegen lijmvoet'
            for u in slot_centres:
                screw = in_ship(upright(u, y, base_z, 3.0, mount['bodemdikte']))
                assert moved.intersect(screw).Volume() < .02, 'M3 past door sleuf'
    for foot, _ in rails:
        assert foot.intersect(motor_hull).Volume() < .02, 'lijmvoet tegen romp'
        assert foot.intersect(hull_joint).Volume() < .02, 'lijmvoet tegen lasstrook'
        assert .05 < foot.distance(motor_hull) < .5, 'lijmspleet'
    for name, part in [('motor', motor_body), ('koppeling', coupling_ref), ('motoras', motor_shaft)]:
        assert part.intersect(bracket_world).Volume() < .02, (name, 'motorsteun')
    assert sleeve_ref.intersect(aft_hull).Volume() > 1, 'de doorvoerbus kruist de beoogde boorlocatie'
    for part in (tube_ref, hub, nut, sweep):
        assert sleeve_ref.intersect(part).Volume() < .02, 'doorvoerbus raakt asbeslag'
    bore = in_ship(on_axis(sleeve['begin_u']-10, sleeve['lengte']+10.5, sleeve['diameter']+.2))
    bored_hull = aft_hull.cut(bore)
    assert len(bored_hull.Solids()) == 1 and bored_hull.isValid(), 'referentieboring scheg'
    assert sleeve_ref.intersect(bored_hull).Volume() < .02, 'bus past niet in de referentieboring'
    assert tube_ref.intersect(hull_joint).Volume() < .02, 'stevenbuis tegen lasstrook'
    assert tube_ref.intersect(motor_hull).Volume() < .02, 'stevenbuis tegen rompdeel 2'
    assert hub.distance(bored_hull) > .1 and hub.distance(rudder) > .1
    assert sweep.BoundingBox().zmin > 0 and sweep.distance(aft_hull) > .1
    for angle in (-45, -35, -20, 0, 20, 35, 45):
        turned = rudder.rotate((23, 0, 0), (23, 0, 1), angle)
        assert sweep.distance(turned) > .1, (angle, 'voorlopige bladzone tegen roer')
        assert hub.intersect(turned).Volume() < .02, (angle, 'naaf tegen roer')

    assembly = cq.Assembly(name='Ortelius p3 - aandrijving')
    parts = [
        ('REFERENTIE rompdeel 1 met virtuele boring', bored_hull, '#163b70', .30),
        ('REFERENTIE rompdeel 2', motor_hull, '#163b70', .30),
        ('REFERENTIE lasstrook 1', hull_joint, '#64758b', .45),
        ('REFERENTIE vast achterdek', rear_deck, '#477d60', .28),
        ('REFERENTIE roer p2', rudder, '#88423a', 1),
        ('PRINT motorsteun', bracket_world, '#bf5d35', 1),
        ('PRINT lijmvoet stuurboord', rails[0][0], '#e5a654', 1),
        ('PRINT lijmvoet bakboord', rails[1][0], '#e5a654', 1),
        ('KOOP motorhuis', motor_body, '#55616e', 1),
        ('KOOP motoras', motor_shaft, '#aeb8bd', 1),
        ('KOOP koppeling', coupling_ref, '#b0adb6', 1),
        ('KOOP stevenbuis', tube_ref, '#c99a4d', 1),
        ('MAATVOORSTEL messing doorvoerbus', sleeve_ref, '#946e28', 1),
        ('KOOP schroefas', shaft_ref, '#c6ccce', 1),
        ('KOOP naaf', hub, '#b8873a', 1),
        ('RESERVE borgmoer', nut, '#b8873a', 1),
        ('RESERVE bladzone', sweep, '#ba913f', .35),
    ]
    for name, solid, color, alpha in parts:
        tint = cq.Color(color).toTuple()
        assembly.add(solid, name=name, color=cq.Color(*tint[:3], alpha))
    path = HERE / 'ortelius-p3-aandrijving.step'
    assembly.export(str(path))
    normalize_step(path)
    reimported = cq.importers.importStep(str(path)).solids().vals()
    assert len(reimported) == len(parts) and all(s.isValid() for s in reimported)

    print(f'{len(reimported)} geldige assemblagedelen, ashoek {ANGLE:.2f} graden')
    print(f'Motorvlak X={in_ship(on_axis(face, .01, .01)).Center().x:.1f} mm')
    print(f'Bladzone: romp {sweep.distance(aft_hull):.2f}, roer middenstand {sweep.distance(rudder):.2f}, '
          f'boven kiel {sweep.BoundingBox().zmin:.2f} mm')
    print(f'Naaf: romp {hub.distance(bored_hull):.2f}, roer {hub.distance(rudder):.2f} mm')


if __name__ == '__main__':
    main()
