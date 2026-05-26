from __future__ import annotations

import cadquery as cq

from spoke_test_rig.cad.params import HubArmParams


def clearance_hole_cutter(diameter: float, length: float) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .circle(diameter / 2.0)
        .extrude(length)
        .translate((0.0, 0.0, -length / 2.0))
    )


def head_counterbore_cutter(params: HubArmParams) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .circle(params.lock_head_diameter / 2.0)
        .extrude(params.lock_head_depth)
        .translate((0.0, 0.0, (params.hub_thickness / 2.0) - params.lock_head_depth))
    )


def nut_trap_cutter(params: HubArmParams) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .polygon(6, params.lock_nut_vertex_diameter)
        .extrude(params.lock_nut_thickness)
        .translate((0.0, 0.0, -params.hub_thickness / 2.0))
    )
