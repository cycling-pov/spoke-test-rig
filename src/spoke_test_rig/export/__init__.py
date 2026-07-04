from __future__ import annotations

from pathlib import Path
from typing import Any

from build123d import export_step, export_stl

from spoke_test_rig.cad.arm import build_arm
from spoke_test_rig.cad.assembly import build_assembly
from spoke_test_rig.cad.hub import build_hub
from spoke_test_rig.cad.params import HubArmParams, QUARTER_INCH_MM, validate_params


def _bbox_lengths(shape: Any) -> tuple[float, float, float]:
    bb = shape.bounding_box()
    return bb.size.X, bb.size.Y, bb.size.Z


def main() -> None:
    params = HubArmParams()
    validate_params(params)

    project_root = Path(__file__).resolve().parents[3]
    export_dir = project_root / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    hub = build_hub(params)
    arm = build_arm(params)
    assembly = build_assembly(params)

    export_step(hub, str(export_dir / "hub.step"))
    export_stl(hub, str(export_dir / "hub.stl"))
    export_step(arm, str(export_dir / "arm.step"))
    export_stl(arm, str(export_dir / "arm.stl"))
    export_step(assembly, str(export_dir / "assembly.step"))

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
            params.hub_thickness,
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
        f"- PCB recess / keep-out (LxW x D): {params.recess_length:.2f} x {params.recess_width:.2f} x {params.recess_depth:.2f} mm",
        f"- PCB standoffs: {params.pcb_standoff_diameter:.2f} mm dia x {params.pcb_standoff_height:.2f} mm tall at {params.pcb_mount_hole_pitch_x:.2f} x {params.pcb_mount_hole_pitch_y:.2f} mm pitch",
        f"- Battery holder backside mount: {params.battery_holder_length:.2f} x {params.battery_holder_width:.2f} mm holder, center offset Y {params.battery_holder_center_y:.2f} mm, {params.battery_holder_mount_pitch_x:.2f} x {params.battery_holder_mount_pitch_y:.2f} mm hole pitch, {params.battery_holder_mount_hole_diameter:.2f} mm pilot holes",
        f"- Bottom hex socket AF: {params.drive_hex_af:.2f} mm (1/4 in)",
        f"- Drive socket insertion depth (effective): {params.drive_socket_depth:.2f} mm",
        f"- Lash holes: {params.lash_hole_count}x {params.lash_hole_diameter:.2f} mm at radius {params.lash_hole_radius:.2f} mm",
        f"- Lash hole rotation: {params.lash_hole_rotation_deg:.2f} deg",
        "- Dovetail placement: sockets centered at 0 and 180 degrees",
        f"- Lock-bolt clearance hole diameter: {params.lock_bolt_clearance_diameter:.2f} mm",
        f"- Lock-head counterbore (D x depth): {params.lock_head_diameter:.2f} x {params.lock_head_depth:.2f} mm",
        f"- Lock-nut trap (AF x depth): {params.lock_nut_flat:.2f} x {params.lock_nut_thickness:.2f} mm",
    ]

    report_path = export_dir / "validation_report.txt"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Exported parts to: {export_dir}")
    print(f"Validation report: {report_path}")


if __name__ == "__main__":
    main()
