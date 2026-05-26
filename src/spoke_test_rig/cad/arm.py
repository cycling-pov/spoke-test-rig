from __future__ import annotations

import cadquery as cq

from spoke_test_rig.cad.lock_bolt import clearance_hole_cutter
from spoke_test_rig.cad.params import HubArmParams, validate_params


def _male_dovetail(params: HubArmParams) -> cq.Workplane:
    tip_w = params.dovetail_inner_width
    shoulder_w = params.dovetail_entry_width

    profile = [
        (-params.dovetail_length, -tip_w / 2.0),
        (-params.dovetail_length, tip_w / 2.0),
        (0.0, shoulder_w / 2.0),
        (0.0, -shoulder_w / 2.0),
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
    shoulder_w = params.dovetail_entry_width

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
            shoulder_w,
            params.arm_thickness,
            centered=(False, True, True),
        )
        .translate((-0.5, 0.0, 0.0))
    )

    arm = body.union(dovetail).union(stop)

    hole_cutter = clearance_hole_cutter(
        params.lock_bolt_clearance_diameter, params.arm_thickness + 2.0
    )

    head_bore = (
        cq.Workplane("XY")
        .circle(params.lock_head_diameter / 2.0)
        .extrude(params.lock_head_depth)
        .translate((0.0, 0.0, (params.arm_thickness / 2.0) - params.lock_head_depth))
    )

    arm = arm.cut(hole_cutter.translate((params.arm_lock_bolt_x, 0.0, 0.0)))
    arm = arm.cut(head_bore.translate((params.arm_lock_bolt_x, 0.0, 0.0)))
    return arm
