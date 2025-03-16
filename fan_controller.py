from copy import copy

from build123d import *  # noqa: F403

cable_gland_diameter = 12.8
knob_diameter = 10

cavity_x = 30
cavity_y = 60
cavity_z = max(cable_gland_diameter, knob_diameter) * 1.75

lid_z = 2.8
lid_lip = 3
lid_tolerance = 0.1
wall_thickness = 2

box_fillet = 4

screw_shaft_radius = 4
screw_head_radius = 8
screw_head_height = 1


def lid_2d():
    return RectangleRounded(
        cavity_x + lid_lip, cavity_y + lid_lip, radius=box_fillet - (wall_thickness / 2)
    )


def inner_box():
    walls = lid_2d() - RectangleRounded(cavity_x, cavity_y, radius=box_fillet - (lid_lip / 2))
    return extrude(walls, amount=cavity_z + wall_thickness)


def outer_box():
    walls = (
        RectangleRounded(
            cavity_x + lid_lip + wall_thickness,
            cavity_y + lid_lip + wall_thickness,
            radius=box_fillet,
        )
        - lid_2d()
    )

    return extrude(walls, amount=cavity_z + lid_z + wall_thickness)


def box_floor():
    floor_2d = RectangleRounded(
        cavity_x + lid_lip + wall_thickness,
        cavity_y + lid_lip + wall_thickness,
        radius=box_fillet,
    )

    return extrude(floor_2d, amount=wall_thickness)


def box():
    box = inner_box() + outer_box() + box_floor()

    cavity_bottom_plane = Plane(box.faces().sort_by(Axis.Z)[1])
    knob_plane = Plane(box.faces().sort_by(Axis.Y)[0])
    cable_gland_plane = Plane(box.faces().sort_by(Axis.Y)[-1])

    box -= [
        cavity_bottom_plane
        * loc
        * CounterBoreHole(
            radius=screw_shaft_radius,
            counter_bore_radius=screw_head_radius,
            counter_bore_depth=screw_head_height,
            depth=wall_thickness,
        )
        for loc in GridLocations(0, cavity_y / 2, 1, 2)
    ]
    box -= knob_plane * Hole(radius=knob_diameter / 2, depth=wall_thickness + lid_lip)
    box -= cable_gland_plane * Hole(radius=cable_gland_diameter / 2, depth=wall_thickness + lid_lip)

    return box


def lid():
    _lid = extrude(offset(lid_2d(), -lid_tolerance), amount=lid_z)
    pry_slot_2d = RectangleRounded(9, (lid_lip - 1) * 2, radius=1)
    pry_slot = extrude(pry_slot_2d, amount=lid_z)

    _lid -= [loc * copy(pry_slot) for loc in GridLocations(0, cavity_y + lid_lip, 1, 2)]

    # Alternatively, if you want to put the pry slots only one side of the lid:
    # edge_center = _lid.edges().sort_by(Axis.Y).filter_by(Plane.XY)[0].center()
    # _lid -= Pos(edge_center.X, edge_center.Y) * pry_slot

    return Pos(1.25 * cavity_x, 0, 0) * _lid


"""
show_object(inner_box())
show_object(outer_box())
show_object(box_floor())
"""
# box()
show_object(box())
show_object(lid())
# show_object(Ellipse(20, lid_lip - 1))
# show_object(inner_box() - outer_box())
# b = Box(20, 20, 20)
# c = Box(20, 20, 20)
# d = b + c
# show_object(d)
