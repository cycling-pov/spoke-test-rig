from __future__ import annotations

import cadquery as cq

from spoke_test_rig.cad.pin import tapered_pin_hole_cutter
from spoke_test_rig.cad.params import HubArmParams, validate_params


def _male_dovetail(params: HubArmParams) -> cq.Workplane:
    profile = [
        (-params.dovetail_length, -params.dovetail_entry_width / 2.0),
        (-params.dovetail_length, params.dovetail_entry_width / 2.0),
        (0.0, params.dovetail_inner_width / 2.0),
        (0.0, -params.dovetail_inner_width / 2.0),
    ]

    return (
        cq.Workplane("XY")
        .polyline(profile)
        .close()
        .extrude(params.arm_thickness)
        .translate((0.0, 0.0, -params.arm_thickness / 2.0))
    )


def build_arm(params: HubArmParams) -> cq.Workplane:
    validate_params(params)

    arm_body_length = params.arm_length - params.dovetail_length

    body = cq.Workplane("XY").box(
        arm_body_length,
        params.arm_width,
        params.arm_thickness,
        centered=(False, True, True),
    )

    dovetail = _male_dovetail(params)

    # Small shoulder where the arm body meets the dovetail controls insertion depth.
    stop = (
        cq.Workplane("XY")
        .box(
            1.0,
            params.dovetail_inner_width,
            params.arm_thickness,
            centered=(False, True, True),
        )
        .translate((-0.5, 0.0, 0.0))
    )

    arm = body.union(dovetail).union(stop)

    hole_cutter = tapered_pin_hole_cutter(params, params.arm_thickness + 2.0)
    return arm.cut(hole_cutter.translate((params.arm_pin_hole_x, 0.0, 0.0)))
