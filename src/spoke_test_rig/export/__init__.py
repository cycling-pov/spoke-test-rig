from __future__ import annotations

from pathlib import Path

import cadquery as cq

from spoke_test_rig.cad.arm import build_arm
from spoke_test_rig.cad.assembly import build_assembly
from spoke_test_rig.cad.hub import build_hub
from spoke_test_rig.cad.params import HubArmParams, QUARTER_INCH_MM, validate_params


def _bbox_lengths(shape: cq.Workplane) -> tuple[float, float, float]:
    bb = shape.val().BoundingBox()
    return bb.xlen, bb.ylen, bb.zlen


def main() -> None:
    params = HubArmParams()
    validate_params(params)

    project_root = Path(__file__).resolve().parents[3]
    export_dir = project_root / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    hub = build_hub(params)
    arm = build_arm(params)
    assembly = build_assembly(params)

    cq.exporters.export(hub, str(export_dir / "hub.step"))
    cq.exporters.export(hub, str(export_dir / "hub.stl"))
    cq.exporters.export(arm, str(export_dir / "arm.step"))
    cq.exporters.export(arm, str(export_dir / "arm.stl"))
    assembly.save(str(export_dir / "assembly.step"))

    arm_x, arm_y, arm_z = _bbox_lengths(arm)
    hub_x, hub_y, hub_z = _bbox_lengths(hub)

    checks = {
        "arm_length_mm": (arm_x, params.arm_length),
        "arm_width_mm": (arm_y, params.arm_width),
        "arm_thickness_mm": (arm_z, params.arm_thickness),
        "hub_diameter_x_mm": (hub_x, params.hub_outer_diameter),
        "hub_diameter_y_mm": (hub_y, params.hub_outer_diameter),
        "hub_total_height_mm": (
            hub_z,
            params.hub_thickness + params.drive_reinforcement_boss_height,
        ),
        "drive_hex_af_mm": (params.drive_hex_af, QUARTER_INCH_MM),
    }

    report_lines = ["# Model Validation"]
    for name, (actual, expected) in checks.items():
        delta = abs(actual - expected)
        report_lines.append(
            f"- {name}: actual={actual:.3f} expected={expected:.3f} delta={delta:.3f}"
        )

    report_lines += [
        "",
        "# Key Fit Targets",
        f"- Breadboard recess (LxW x D): {params.recess_length:.2f} x {params.recess_width:.2f} x {params.recess_depth:.2f} mm",
        f"- Bottom hex socket AF: {params.drive_hex_af:.2f} mm (1/4 in)",
        f"- Drive socket insertion depth (effective): {params.drive_socket_depth + params.drive_reinforcement_boss_height:.2f} mm",
        f"- Drive reinforcement boss (D x H): {params.drive_reinforcement_boss_diameter:.2f} x {params.drive_reinforcement_boss_height:.2f} mm",
        f"- Lash holes: {params.lash_hole_count}x {params.lash_hole_diameter:.2f} mm at radius {params.lash_hole_radius:.2f} mm",
        f"- Lash hole rotation: {params.lash_hole_rotation_deg:.2f} deg",
        f"- Dovetail placement: sockets centered at 0 and 180 degrees",
    ]

    report_path = export_dir / "validation_report.txt"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Exported parts to: {export_dir}")
    print(f"Validation report: {report_path}")


if __name__ == "__main__":
    main()
