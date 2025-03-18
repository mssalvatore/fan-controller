import argparse
from copy import copy
from pathlib import Path

from build123d import *  # noqa: F403
from ocp_vscode import (  # noqa: F401
    get_defaults,
    reset_show,
    set_defaults,
    set_port,
    show,
    show_all,
    show_object,
)

set_port(3939)

cable_gland_radius = 12.8 / 2
knob_radius = 8 / 2

cavity_x = 30
cavity_y = 60
cavity_z = 25

lid_z = 2.8
lid_lip = 3
lid_tolerance = 0.1
wall_thickness = 2

box_fillet = 6

screw_shaft_radius = 4.5 / 2
screw_head_radius = 8.6 / 2
screw_head_height = 1


def lid_2d():
    return RectangleRounded(
        cavity_x + lid_lip, cavity_y + lid_lip, radius=box_fillet - (wall_thickness / 2)
    )


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
    box -= knob_plane * Hole(radius=knob_radius, depth=wall_thickness + lid_lip)
    box -= cable_gland_plane * Hole(radius=cable_gland_radius, depth=wall_thickness + lid_lip)

    return box


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


def lid():
    _lid = extrude(offset(lid_2d(), -lid_tolerance), amount=lid_z)
    pry_slot_2d = RectangleRounded(9, (lid_lip - 1) * 2, radius=1)
    pry_slot = extrude(pry_slot_2d, amount=lid_z)

    _lid -= [loc * copy(pry_slot) for loc in GridLocations(0, cavity_y + lid_lip, 1, 2)]

    # Alternatively, if you want to put the pry slots only one side of the lid:
    # edge_center = _lid.edges().sort_by(Axis.Y).filter_by(Plane.XY)[0].center()
    # _lid -= Pos(edge_center.X, edge_center.Y) * pry_slot

    return _lid


def export_model_to_stl(model: Part):
    src_file_path = Path(__file__)
    renders_dir = src_file_path.parent.parent / "renders"

    if not renders_dir.exists():
        renders_dir.mkdir()
    elif not renders_dir.is_dir():
        raise RuntimeError(f"{renders_dir} is not a directory.")

    stl_file_name = src_file_path.stem + ".stl"

    export_stl(model, renders_dir / stl_file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple fan controller for one PC case fan.")
    parser.add_argument("--stl", action="store_true", help="Export STL")
    args = parser.parse_args()

    model = Part() + pack([box(), lid()], padding=10)

    if args.stl:
        export_model_to_stl(Part() + model)
    else:
        show_all()
