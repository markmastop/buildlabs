"""Parametric photographic wheelhouse; dimensions remain prototype assumptions."""
import math
import cadquery as cq

def _wire(points,z):
    return cq.Workplane('XY').polyline(points).close().wire().val().translate(cq.Vector(0,0,z))

def _offset(wire,distance,z):
    result=cq.Workplane('XY').add(wire).toPending().offset2D(distance,kind='intersection').val() if distance else wire
    return result.translate(cq.Vector(0,0,z-result.BoundingBox().zmin))

def _outline(cfg,upper=False):
    front=cfg['front_top_x'] if upper else cfg['front_base_x']
    shoulder=cfg['shoulder_top_x'] if upper else cfg['shoulder_base_x']
    a=cfg['front_flat_halfwidth'];hw=cfg['halfwidth'];rear=cfg['rear_x'];rr=cfg['rear_corner_radius'];n=cfg['corner_segments']
    pts=[(front,-a)]
    for i in range(1,n+1):
        t=math.pi/2*i/n;pts.append((front+(shoulder-front)*(1-math.cos(t)),-a-(hw-a)*math.sin(t)))
    pts.append((rear-rr,-hw))
    for i in range(1,n+1):
        t=math.pi/2*i/n;pts.append((rear-rr+rr*math.sin(t),-hw+rr*(1-math.cos(t))))
    pts.append((rear,hw-rr))
    for i in range(1,n+1):
        t=math.pi/2*i/n;pts.append((rear-rr*(1-math.cos(t)),hw-rr+rr*math.sin(t)))
    pts.append((shoulder,hw))
    for i in range(n-1,-1,-1):
        t=math.pi/2*i/n;pts.append((front+(shoulder-front)*(1-math.cos(t)),a+(hw-a)*math.sin(t)))
    return pts

def _local_roundrect(w,h,depth,radius):
    return cq.Workplane('XY').box(w,h,depth,centered=(True,True,True)).edges('|Z').fillet(radius)

def _placed(shape,origin,normal):
    nx,ny,nz=normal
    plane=cq.Plane(origin=origin,xDir=(-ny,nx,0),normal=normal)
    return cq.Workplane(obj=shape.val().transformShape(plane.rG))

def make_bridge(cfg):
    z=cfg['base_z'];height=cfg['height'];top=z+height;lean=z+cfg['lean_start'];wall=cfg['wall']
    bottom=_wire(_outline(cfg),0);upper=_wire(_outline(cfg,True),0)
    def body_loft(offset,extra=0):
        return cq.Workplane(obj=cq.Solid.makeLoft([_offset(bottom,offset,z-extra),_offset(bottom,offset,lean),_offset(upper,offset,top+extra)],ruled=True))
    outer=body_loft(0);inner=body_loft(-wall,1);body=outer.cut(inner)
    relief_skin=body_loft(cfg['frame_relief']).cut(body_loft(-.2))
    windows=[]
    def window(name,origin,normal,w,h):
        nonlocal body
        fw=cfg['frame_width'];radius=cfg['window_radius']
        outside=_local_roundrect(w+2*fw,h+2*fw,42,radius+fw)
        inside=_local_roundrect(w,h,44,radius)
        body=body.union(_placed(outside.cut(inside),origin,normal).intersect(relief_skin))
        cutter=_placed(inside,origin,normal);body=body.cut(cutter)
        windows.append(dict(name=name,center=list(origin),normal=list(normal),width=w,height=h,opening_bottom=origin[2]-h/2))
    wb=z+cfg['window_bottom'];wh=cfg['window_height'];mid=wb+wh/2
    fraction=(mid-lean)/(top-lean)
    xf=cfg['front_base_x']+(cfg['front_top_x']-cfg['front_base_x'])*fraction
    shoulder=cfg['shoulder_base_x']+(cfg['shoulder_top_x']-cfg['shoulder_base_x'])*fraction
    for y in cfg['front_window_y']:
        # The two outer panes follow the curved wall tangent, instead of sharing
        # the broad flat front plane. The central pair remains on the centre flat.
        if abs(y)<=cfg['front_flat_halfwidth']:
            px=xf;normal=(-1,0,0)
        else:
            t=math.asin((abs(y)-cfg['front_flat_halfwidth'])/(cfg['halfwidth']-cfg['front_flat_halfwidth']))
            px=xf+(shoulder-xf)*(1-math.cos(t))
            nx=-math.cos(t)/(shoulder-xf);ny=math.copysign(math.sin(t)/(cfg['halfwidth']-cfg['front_flat_halfwidth']),y);ll=math.hypot(nx,ny)
            normal=(nx/ll,ny/ll,0)
        window('front_'+str(y),(px,y,mid),normal,cfg['front_window_width'],wh)
    def corner_aperture(points,y,expand=0):
        work=cq.Workplane('XZ',origin=(0,y,0)).polyline(points).close()
        if expand:work=work.offset2D(expand,kind='intersection')
        return work.extrude(cfg['corner_aperture_half_depth'],both=True).edges('|Y').fillet(cfg['window_radius']+expand)
    corner_points=[(x,z+zz) for x,zz in cfg['corner_window_profile_xz']]
    for sign in [-1,1]:
        yy=sign*cfg['halfwidth'];hole=corner_aperture(corner_points,yy)
        rim=corner_aperture(corner_points,yy,cfg['frame_width']).cut(hole)
        body=body.union(rim.intersect(relief_skin)).cut(hole)
        windows.append(dict(name='sloped_corner_'+str(sign),center=[47.5,sign*67.5,z+40],normal=[0,sign,0],profile_xz=corner_points,extrusion_plane_y=yy,opening_bottom=z+cfg['corner_window_profile_xz'][0][1]))
        for sw in cfg['side_windows']:
            smid=z+sw['bottom']+sw['height']/2
            window('side_'+str(sign)+'_'+str(sw['x']),(sw['x'],sign*cfg['halfwidth'],smid),(0,sign,0),sw['width'],sw['height'])
        # Door is a closed lower panel with a window, mirrored about the centreline.
        dc=(cfg['door_center_x'],sign*cfg['halfwidth'],z+cfg['door_bottom']+cfg['door_height']/2)
        border=_local_roundrect(cfg['door_width'],cfg['door_height'],42,cfg['door_radius']).cut(_local_roundrect(cfg['door_width']-2*cfg['door_frame_width'],cfg['door_height']-2*cfg['door_frame_width'],44,max(.15,cfg['door_radius']-cfg['door_frame_width'])))
        body=body.union(_placed(border,dc,(0,sign,0)).intersect(relief_skin))
        handle=cq.Workplane('XY').box(1.8,.9,.6,centered=(True,True,False)).translate((0,0,-.2))
        body=body.union(_placed(handle,(cfg['door_center_x']+cfg['door_handle_offset'],sign*cfg['halfwidth'],z+cfg['door_handle_height']),(0,sign,0)))
    rear=cfg['rear_x']
    for y in cfg['rear_outer_window_y']:
        window('rear_outer_'+str(y),(rear,y,z+cfg['rear_outer_window_bottom']+cfg['rear_outer_window_height']/2),(1,0,0),cfg['rear_outer_window_width'],cfg['rear_outer_window_height'])
    for y in cfg['rear_tall_window_y']:
        rh=cfg['rear_tall_window_height'];rb=z+cfg['rear_tall_window_bottom']
        window('rear_tall_'+str(y),(rear,y,rb+rh/2),(1,0,0),cfg['rear_tall_window_width'],rh)
    # Keep the intended hollow wall and all apertures clear after adding surrounds.
    body=body.cut(inner)
    for win in windows:
        if 'profile_xz' in win:body=body.cut(corner_aperture(win['profile_xz'],win['extrusion_plane_y']))
        else:body=body.cut(_placed(_local_roundrect(win['width'],win['height'],44,cfg['window_radius']),win['center'],win['normal']))

    # Roof eaves follow the rounded wheelhouse; cap stays separate for glazing.
    eave=_offset(upper,cfg['roof_overhang'],top)
    plate=cq.Workplane('XY').add(eave).toPending().extrude(cfg['roof_plate'])
    hz=top+cfg['roof_plate'];hoodtop=hz+cfg['hood_height'];split=hoodtop-cfg['cap_thickness']
    hood_plan=cq.Workplane('XY').add(_offset(eave,0,0)).toPending().extrude(1)
    hood_plan=hood_plan.intersect(cq.Workplane('XY').box(400,400,3,centered=(False,True,False)).translate((cfg['hood_rear_x']-400,0,-1)))
    hb=hood_plan.faces('<Z').wires().val();ht=_offset(hb,-cfg['hood_inset'],0)
    def hood_loft(inset,extra=0):
        return cq.Workplane(obj=cq.Solid.makeLoft([_offset(hb,inset,hz-extra),_offset(ht,inset,hoodtop+extra)],ruled=True))
    hout=hood_loft(0);hin=hood_loft(-cfg['hood_wall'],1)
    hood=hout.cut(hin)
    hoodskin=hood_loft(cfg['frame_relief']).cut(hood_loft(-.2))
    roof_windows=[]
    for y in cfg['hood_window_y']:
        zz=hz+cfg['hood_window_center_height'];xx=cfg['hood_rear_x']-cfg['hood_inset']*(zz-hz)/cfg['hood_height']
        origin=(xx,y,zz);normal=(1,0,0);w=cfg['hood_window_width'];h=cfg['hood_window_height'];fw=cfg['frame_width']
        hole=_local_roundrect(w,h,44,.8)
        rim=_local_roundrect(w+2*fw,h+2*fw,42,.8+fw).cut(hole)
        hood=hood.union(_placed(rim,origin,normal).intersect(hoodskin)).cut(_placed(hole,origin,normal))
        roof_windows.append(dict(center=list(origin),width=w,height=h))
    hood=hood.intersect(cq.Workplane('XY').box(500,500,split-hz,centered=(True,True,False)).translate((0,0,hz))).cut(hin)
    hole=cq.Workplane('XY').add(_offset(hb,-3.5,top-1)).toPending().extrude(cfg['roof_plate']+3)
    roof=plate.cut(hole).union(hood)
    cap=hout.intersect(cq.Workplane('XY').box(500,500,cfg['cap_thickness'],centered=(True,True,False)).translate((0,0,split)))
    cap_edge=_offset(ht,0,hoodtop)
    report=dict(proportions=dict(wall_height=cfg['height'],foot_length=cfg['rear_x']-cfg['front_base_x'],width=2*cfg['halfwidth'],added_height_under_windows=13),symmetry_confirmed_by_user=True,front_revision=dict(flat_width=2*cfg['front_flat_halfwidth'],outer_panes_follow_local_tangent=True,roof_overhang=cfg['roof_overhang']),rear_three_tall_openings_confirmed=True,windows=windows,roof_windows=roof_windows,body_base_z=z,body_top_z=top,hood_top_z=hoodtop,cap_bottom_z=split,door=dict(rectangular=True,center_x=cfg['door_center_x'],width=cfg['door_width'],bottom=z+cfg['door_bottom'],height=cfg['door_height'],closed_lower_panel=True),separate_forward_window=dict(sloped_fore_stile=True,profile_xz=corner_points),roof_revision=dict(hood_rear_x=cfg['hood_rear_x'],hood_height=cfg['hood_height'],flat_aft_roof_length=cfg['rear_x']+cfg['roof_overhang']-cfg['hood_rear_x']),dimensions_status='photographic prototype dimensions, not measured')
    for name,shape in [('body',body),('roof',roof),('cap',cap)]:
        shape=shape.clean();assert len(shape.solids().vals())==1 and shape.val().isValid(),(name,'disconnected or invalid')
    return body.clean(),roof.clean(),cap.clean(),report,cap_edge
