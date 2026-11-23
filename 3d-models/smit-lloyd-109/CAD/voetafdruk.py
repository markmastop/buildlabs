"""Voetafdruk van het onderdekhuis, gedeeld door build.py en pasmal/maak_pasmal.py.

Interne coördinaten in mm: X=0 is de punt van de neus, X loopt naar achteren,
Y=0 is de hartlijn. +Y is de kant met het brede blok (exportassen spiegelen Y).
Hoeken krijgen een afronding als polylijn, net als de neusellips: rechte
segmenten houden de STEP-uitwisseling betrouwbaar.
"""
import math


def stations(P):
    M, C = P['measured'], P['construction']
    s = {}
    s['L'] = L = M['length']
    s['H'] = H = C['aft_halfwidth']
    s['nr'] = C['fore_nose_depth']
    s['half_front'] = M['front_width'] / 2
    s['yiL'] = yiL = -H + M['left_narrow']
    s['yiR'] = yiR = yiL + M['U_width']
    s['UX'] = UX = L - M['U_depth_left']
    s['l3'], s['l4'] = L - M['left_F3'], L - M['left_F4']
    s['r3'], s['r4'] = L - M['right_F3'], L - M['right_F4']
    s['lout'] = yiL - M['left_wide']
    s['rib'] = rib = H - M['right_bare']
    s['rheadinner'] = rheadinner = rib + C['right_shoulder_lateral_shift']
    s['rheadouter'] = rheadinner + M['right_wide']
    s['rtaper'] = rheadinner + M['right_bare']
    # Het brede blok eindigt aan de U-kant op de gemeten 60 mm vanaf de U-bodem.
    # Aan de armkant is een inkeping uitgespaard (fotomaat, v18).
    s['nt'] = nt = UX + M['U_to_low_block']
    s['notch_x'] = nt - C['small_notch_length']
    s['notch_y'] = rheadinner - C['small_notch_width']
    # Binnenkant van beide armen loopt over de laatste mm's schuin naar buiten.
    s['taper_x'] = L - C['arm_inner_taper_length']
    s['left_end_inner'] = yiL - C['left_arm_inner_taper']
    s['right_end_inner'] = rheadinner + C['right_arm_inner_taper']
    assert abs(H - yiR - M['right_with_block']) < .001
    assert yiR < s['notch_y'] < rheadinner and UX < s['notch_x'] < nt
    return s


def nose_points(P, width=None):
    C = P['construction']
    n, nr = C['fore_nose_segments'], C['fore_nose_depth']
    yy = (P['measured']['front_width'] if width is None else width) / 2
    return [(nr - nr * math.cos(-math.pi / 2 + i * math.pi / n),
             yy * math.sin(-math.pi / 2 + i * math.pi / n)) for i in range(n + 1)]


def rounded_polygon(corners, step_degrees=7.5):
    """Vervang hoekpunten (x, y, r) met r > 0 door een raakboog met straal r."""
    pts = [(x, y) for x, y, _ in corners]
    radii = [r for _, _, r in corners]
    n = len(pts)
    tangent = [0.0] * n
    geometry = [None] * n
    for i, (p, r) in enumerate(zip(pts, radii)):
        if not r:
            continue
        a, b = pts[i - 1], pts[(i + 1) % n]
        u = (a[0] - p[0], a[1] - p[1]); lu = math.hypot(*u); u = (u[0] / lu, u[1] / lu)
        v = (b[0] - p[0], b[1] - p[1]); lv = math.hypot(*v); v = (v[0] / lv, v[1] / lv)
        theta = math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1])))
        t = r / math.tan(theta / 2)
        bis = (u[0] + v[0], u[1] + v[1]); lb = math.hypot(*bis); bis = (bis[0] / lb, bis[1] / lb)
        d = r / math.sin(theta / 2)
        centre = (p[0] + bis[0] * d, p[1] + bis[1] * d)
        tangent[i] = t
        geometry[i] = (centre, (p[0] + u[0] * t, p[1] + u[1] * t), (p[0] + v[0] * t, p[1] + v[1] * t))
    for i in range(n):
        j = (i + 1) % n
        length = math.dist(pts[i], pts[j])
        assert tangent[i] + tangent[j] <= length + 1e-9, ('afronding past niet', pts[i], pts[j])
    out = []
    for i, p in enumerate(pts):
        if geometry[i] is None:
            out.append(p)
            continue
        (cx, cy), p1, p2 = geometry[i]
        r = radii[i]
        a1 = math.atan2(p1[1] - cy, p1[0] - cx)
        a2 = math.atan2(p2[1] - cy, p2[0] - cx)
        sweep = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
        steps = max(2, math.ceil(abs(sweep) / math.radians(step_degrees)))
        out += [(cx + r * math.cos(a1 + sweep * k / steps), cy + r * math.sin(a1 + sweep * k / steps))
                for k in range(steps + 1)]
    return out


def outline_points(P):
    """Gesloten omtrek van het onderdekhuis als lijst (x, y)-punten."""
    M, C = P['measured'], P['construction']
    s = stations(P)
    L, H, UX = s['L'], s['H'], s['UX']
    R, Rn, Ru = C['end_radius'], C['notch_corner_radius'], C['U_corner_radius']
    hf = s['half_front']
    corners = [(x, y, 0) for x, y in nose_points(P)]
    corners += [
        (M['fore_roof_length'], hf, 0), (UX, H, 0), (s['r4'], H, 0),
        (s['r3'], s['rheadouter'], 0), (C['rear_taper_start'], s['rtaper'], 0),
        (L, s['rtaper'], R), (L, s['right_end_inner'], R),
        (s['taper_x'], s['rheadinner'], 0),
        (s['notch_x'], s['rheadinner'], Rn), (s['notch_x'], s['notch_y'], Rn),
        (s['nt'], s['notch_y'], Rn), (s['nt'], s['yiR'], Rn),
        (UX, s['yiR'], Ru), (UX, s['yiL'], Ru),
        (s['taper_x'], s['yiL'], 0), (L, s['left_end_inner'], R),
        (L, s['lout'], R), (s['l3'], s['lout'], 0), (s['l4'], -H, 0), (UX, -H, 0),
        (M['fore_roof_length'], -hf, 0),
    ]
    return rounded_polygon(corners)
