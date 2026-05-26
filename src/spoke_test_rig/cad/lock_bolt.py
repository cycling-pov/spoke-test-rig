from __future__ import annotations

from build123d import BuildSketch, Cylinder, Plane, Pos, RegularPolygon, extrude

from spoke_test_rig.cad.params import HubArmParams


def clearance_hole_cutter(diameter: float, length: float) -> Cylinder:
    return Cylinder(diameter / 2.0, length)


def head_counterbore_cutter(params: HubArmParams) -> Cylinder:
    return Pos(
        0.0, 0.0, (params.hub_thickness / 2.0) - (params.lock_head_depth / 2.0)
    ) * Cylinder(
        params.lock_head_diameter / 2.0,
        params.lock_head_depth,
    )


def nut_trap_cutter(params: HubArmParams):
    with BuildSketch(Plane.XY) as hex_profile:
        RegularPolygon(params.lock_nut_vertex_diameter / 2.0, 6)

    nut_trap = Pos(
        0.0,
        0.0,
        -params.hub_thickness / 2.0 + (params.lock_nut_thickness / 2.0),
    ) * extrude(hex_profile.sketch, amount=params.lock_nut_thickness)
    return nut_trap.solid()
