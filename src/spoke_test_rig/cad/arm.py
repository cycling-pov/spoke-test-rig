from __future__ import annotations

from build123d import (
    Align,
    Box,
    BuildPart,
    BuildLine,
    BuildSketch,
    Cylinder,
    Mode,
    Locations,
    Plane,
    Polyline,
    extrude,
    make_face,
)

from spoke_test_rig.cad.params import HubArmParams, validate_params


def _male_dovetail(params: HubArmParams):
    tip_w = params.dovetail_inner_width
    shoulder_w = params.dovetail_entry_width

    with BuildPart() as dovetail:
        with BuildSketch(Plane.XY.offset(-params.arm_thickness / 2.0)):
            with BuildLine():
                Polyline(
                    (-params.dovetail_length, -tip_w / 2.0),
                    (-params.dovetail_length, tip_w / 2.0),
                    (0.0, shoulder_w / 2.0),
                    (0.0, -shoulder_w / 2.0),
                    close=True,
                )
            make_face()
        extrude(amount=params.arm_thickness)

    part = dovetail.part
    assert part is not None
    return part


def build_arm(params: HubArmParams):
    validate_params(params)

    arm_body_length = params.arm_length - params.dovetail_length
    shoulder_w = params.dovetail_entry_width

    with BuildPart() as arm:
        Box(
            arm_body_length,
            params.arm_width,
            params.arm_thickness,
            align=(Align.MIN, Align.CENTER, Align.CENTER),
        )

        with BuildSketch(Plane.XY.offset(-params.arm_thickness / 2.0)):
            with BuildLine():
                Polyline(
                    (-params.dovetail_length, -params.dovetail_inner_width / 2.0),
                    (-params.dovetail_length, params.dovetail_inner_width / 2.0),
                    (0.0, params.dovetail_entry_width / 2.0),
                    (0.0, -params.dovetail_entry_width / 2.0),
                    close=True,
                )
            make_face()
        extrude(amount=params.arm_thickness)

        # Small shoulder where the arm body meets the dovetail controls insertion depth.
        Box(1.0, shoulder_w, params.arm_thickness)

        with Locations((params.arm_lock_bolt_x, 0.0, 0.0)):
            Cylinder(
                params.lock_bolt_clearance_diameter / 2.0,
                params.arm_thickness + 2.0,
                mode=Mode.SUBTRACT,
            )

        with Locations(
            (
                params.arm_lock_bolt_x,
                0.0,
                (params.arm_thickness / 2.0) - (params.lock_head_depth / 2.0),
            )
        ):
            Cylinder(
                params.lock_head_diameter / 2.0,
                params.lock_head_depth,
                mode=Mode.SUBTRACT,
            )

    part = arm.part
    assert part is not None
    return part
