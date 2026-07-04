from __future__ import annotations

import math
from build123d import (
    BuildPart,
    BuildLine,
    BuildSketch,
    Cylinder,
    Locations,
    Mode,
    Plane,
    RegularPolygon,
    Rectangle,
    extrude,
    make_face,
    Polyline,
)

from spoke_test_rig.cad.params import HubArmParams, validate_params


def _lash_hole_points(
    radius: float, count: int, rotation_deg: float
) -> list[tuple[float, float]]:
    # Rotate the evenly spaced pattern so no hole lands on 0/180 dovetail directions.
    step = 360.0 / float(count)
    angles_deg = [rotation_deg + (i * step) for i in range(count)]
    return [
        (radius * math.cos(math.radians(a)), radius * math.sin(math.radians(a)))
        for a in angles_deg
    ]


def _pcb_standoff_points(params: HubArmParams) -> list[tuple[float, float]]:
    x = params.pcb_hole_offset_x
    y = params.pcb_hole_offset_y
    return [(x, y), (x, -y), (-x, y), (-x, -y)]


def _battery_holder_mount_points(params: HubArmParams) -> list[tuple[float, float]]:
    x = params.battery_holder_hole_offset_x
    y = params.battery_holder_hole_offset_y
    center_y = params.battery_holder_center_y
    return [
        (x, center_y + y),
        (x, center_y - y),
        (-x, center_y + y),
        (-x, center_y - y),
    ]


def build_hub(params: HubArmParams):
    validate_params(params)

    radius = params.hub_outer_diameter / 2.0
    entry_w = params.dovetail_entry_width + (2.0 * params.dovetail_xy_clearance)
    inner_w = params.dovetail_inner_width + (2.0 * params.dovetail_xy_clearance)
    socket_center_z = (params.hub_thickness - params.dovetail_socket_height) / 2.0
    socket_base_z = socket_center_z - (params.dovetail_socket_height / 2.0)

    with BuildPart() as hub:
        Cylinder(radius, params.hub_thickness)

        # PCB locating posts on the top face.
        with Locations(
            [
                (
                    x,
                    y,
                    (params.hub_thickness / 2.0) + (params.pcb_standoff_height / 2.0),
                )
                for x, y in _pcb_standoff_points(params)
            ]
        ):
            Cylinder(
                params.pcb_standoff_diameter / 2.0,
                params.pcb_standoff_height,
                mode=Mode.ADD,
            )

        # Dual battery holder pilot holes on the backside.
        with Locations(
            _battery_holder_mount_points(params)
        ):
            Cylinder(
                params.battery_holder_mount_hole_diameter / 2.0,
                params.hub_thickness + 2.0,
                mode=Mode.SUBTRACT,
            )

        # Hex nut recess on the top side for the battery-holder screws.
        with BuildSketch(
            Plane.XY.offset((params.hub_thickness / 2.0) - params.battery_holder_nut_depth)
        ):
            with Locations(_battery_holder_mount_points(params)):
                RegularPolygon(params.battery_holder_nut_vertex_diameter / 2.0, 6)
        extrude(amount=params.battery_holder_nut_depth, mode=Mode.SUBTRACT)

        # Bottom 1/4-inch hex socket plus lead-in opening.
        with BuildSketch(Plane.XY.offset(-params.hub_thickness / 2.0)):
            RegularPolygon(params.hex_leadin_radius, 6)
        extrude(amount=params.drive_leadin_depth, mode=Mode.SUBTRACT)

        with BuildSketch(
            Plane.XY.offset(-params.hub_thickness / 2.0 + params.drive_leadin_depth)
        ):
            RegularPolygon(params.hex_radius, 6)
        extrude(amount=params.drive_socket_depth, mode=Mode.SUBTRACT)

        with Locations(
            _lash_hole_points(
                params.lash_hole_radius,
                params.lash_hole_count,
                params.lash_hole_rotation_deg,
            )
        ):
            Cylinder(
                params.lash_hole_diameter / 2.0,
                params.hub_thickness + 2.0,
                mode=Mode.SUBTRACT,
            )

        # Opposing female dovetail sockets at 180 degrees, flush with the top face.
        with BuildSketch(Plane.XY.offset(socket_base_z)):
            with BuildLine():
                Polyline(
                    (radius + params.dovetail_socket_entry_offset, -entry_w / 2.0),
                    (radius + params.dovetail_socket_entry_offset, entry_w / 2.0),
                    (radius - params.dovetail_length, inner_w / 2.0),
                    (radius - params.dovetail_length, -inner_w / 2.0),
                    close=True,
                )
            make_face()
        extrude(amount=params.dovetail_socket_height, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XY.offset(socket_base_z)):
            with BuildLine():
                Polyline(
                    (-radius - params.dovetail_socket_entry_offset, -entry_w / 2.0),
                    (-radius - params.dovetail_socket_entry_offset, entry_w / 2.0),
                    (-radius + params.dovetail_length, inner_w / 2.0),
                    (-radius + params.dovetail_length, -inner_w / 2.0),
                    close=True,
                )
            make_face()
        extrude(amount=params.dovetail_socket_height, mode=Mode.SUBTRACT)

        # Through-bolt retention at each arm/hub dovetail interface.
        with Locations(
            (params.hub_lock_bolt_x, 0.0, 0.0), (-params.hub_lock_bolt_x, 0.0, 0.0)
        ):
            Cylinder(
                params.lock_bolt_clearance_diameter / 2.0,
                params.hub_thickness + 2.0,
                mode=Mode.SUBTRACT,
            )

        with BuildSketch(Plane.XY.offset(-params.hub_thickness / 2.0)):
            with Locations(
                (params.hub_lock_bolt_x, 0.0), (-params.hub_lock_bolt_x, 0.0)
            ):
                RegularPolygon(params.lock_nut_vertex_diameter / 2.0, 6)
        extrude(amount=params.lock_nut_thickness, mode=Mode.SUBTRACT)

    part = hub.part
    assert part is not None
    return part
