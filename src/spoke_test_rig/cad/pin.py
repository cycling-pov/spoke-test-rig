from __future__ import annotations

import cadquery as cq

from spoke_test_rig.cad.params import HubArmParams, validate_params


def tapered_pin_hole_cutter(params: HubArmParams, length: float) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .workplane(offset=-length / 2.0)
        .circle(params.pin_hole_bottom_diameter / 2.0)
        .workplane(offset=length)
        .circle(params.pin_hole_top_diameter / 2.0)
        .loft(combine=True)
    )


def build_pin(params: HubArmParams) -> cq.Workplane:
    validate_params(params)

    return (
        cq.Workplane("XY")
        .workplane(offset=-params.pin_length / 2.0)
        .circle(params.pin_bottom_diameter / 2.0)
        .workplane(offset=params.pin_length)
        .circle(params.pin_top_diameter / 2.0)
        .loft(combine=True)
    )
