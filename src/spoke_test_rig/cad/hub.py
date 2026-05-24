from __future__ import annotations

import math
import cadquery as cq

from spoke_test_rig.cad.params import HubArmParams, validate_params


def _female_dovetail_cutter(params: HubArmParams) -> cq.Workplane:
    entry_w = params.dovetail_entry_width + (2.0 * params.dovetail_xy_clearance)
    inner_w = params.dovetail_inner_width + (2.0 * params.dovetail_xy_clearance)

    profile = [
        (params.dovetail_socket_entry_offset, -entry_w / 2.0),
        (params.dovetail_socket_entry_offset, entry_w / 2.0),
        (-params.dovetail_length, inner_w / 2.0),
        (-params.dovetail_length, -inner_w / 2.0),
    ]

    return (
        cq.Workplane("XY")
        .polyline(profile)
        .close()
        .extrude(params.dovetail_socket_height)
        .translate((0.0, 0.0, -params.dovetail_socket_height / 2.0))
    )


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


def build_hub(params: HubArmParams) -> cq.Workplane:
    validate_params(params)

    radius = params.hub_outer_diameter / 2.0

    hub = (
        cq.Workplane("XY")
        .circle(radius)
        .extrude(params.hub_thickness)
        .translate((0.0, 0.0, -params.hub_thickness / 2.0))
    )

    # Breadboard recess on top.
    hub = (
        hub.faces(">Z")
        .workplane()
        .rect(params.recess_length, params.recess_width)
        .cutBlind(-params.recess_depth)
    )

    # Reinforcement boss at the bottom drive interface.
    boss = (
        cq.Workplane("XY")
        .circle(params.drive_reinforcement_boss_diameter / 2.0)
        .extrude(params.drive_reinforcement_boss_height)
        .translate(
            (
                0.0,
                0.0,
                -params.hub_thickness / 2.0 - params.drive_reinforcement_boss_height,
            )
        )
    )
    hub = hub.union(boss)

    # Bottom 1/4-inch hex socket plus lead-in opening.
    # Cut starts at boss bottom so effective insertion depth increases.
    leadin = (
        cq.Workplane("XY")
        .polygon(6, 2.0 * params.hex_leadin_radius)
        .extrude(params.drive_leadin_depth + params.drive_reinforcement_boss_height)
        .translate(
            (
                0.0,
                0.0,
                -params.hub_thickness / 2.0 - params.drive_reinforcement_boss_height,
            )
        )
    )

    hex_core = (
        cq.Workplane("XY")
        .polygon(6, 2.0 * params.hex_radius)
        .extrude(params.drive_socket_depth + params.drive_reinforcement_boss_height)
        .translate(
            (
                0.0,
                0.0,
                -params.hub_thickness / 2.0
                - params.drive_reinforcement_boss_height
                + params.drive_leadin_depth,
            )
        )
    )

    hub = hub.cut(leadin).cut(hex_core)

    hub = (
        hub.faces(">Z")
        .workplane()
        .pushPoints(
            _lash_hole_points(
                params.lash_hole_radius,
                params.lash_hole_count,
                params.lash_hole_rotation_deg,
            )
        )
        .hole(params.lash_hole_diameter)
    )

    # Opposing female dovetail sockets at 180 degrees.
    socket = _female_dovetail_cutter(params).translate((radius, 0.0, 0.0))
    opposite_socket = socket.mirror("YZ")

    return hub.cut(socket).cut(opposite_socket)
