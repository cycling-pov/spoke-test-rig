from __future__ import annotations

from dataclasses import dataclass
import math


INCH_TO_MM = 25.4
QUARTER_INCH_MM = 0.25 * INCH_TO_MM


@dataclass(frozen=True)
class HubArmParams:
    # PCB nominal dimensions.
    pcb_length: float = 56.0
    pcb_width: float = 47.0
    pcb_thickness: float = 1.6
    pcb_mount_hole_pitch_x: float = 42.0
    pcb_mount_hole_pitch_y: float = 42.0
    pcb_mount_hole_diameter: float = 2.2
    pcb_standoff_diameter: float = 2.0
    pcb_standoff_height: float = 2.5

    # Dual battery holder backside mount.
    battery_holder_length: float = 78.0
    battery_holder_width: float = 42.0
    battery_holder_mount_pitch_x: float = 55.5
    battery_holder_mount_pitch_y: float = 21.40
    battery_holder_mount_hole_diameter: float = 2.8
    battery_holder_center_offset_y: float = -26.0
    battery_holder_nut_flat: float = 5.8
    battery_holder_nut_depth: float = 2.8

    # Assembly-fit clearances tuned for PLA/PETG FDM.
    recess_xy_clearance: float = 0.5
    recess_z_clearance: float = 0.4
    recess_floor_thickness: float = 3.0
    dovetail_xy_clearance: float = 0.1
    dovetail_z_clearance: float = 0.08

    # Hub geometry.
    hub_thickness: float = 21.1
    hub_outer_diameter: float = 100.0
    hub_wall_margin: float = 10.0

    # Bottom drive socket geometry.
    drive_hex_af: float = QUARTER_INCH_MM
    drive_socket_depth: float = 8.0
    drive_leadin_depth: float = 1.2
    drive_leadin_delta_af: float = 0.8

    # Battery lashing holes near hub perimeter.
    lash_hole_count: int = 4
    lash_hole_diameter: float = 4.0
    lash_hole_radial_inset: float = 11.0
    lash_hole_rotation_deg: float = 45.0

    # Arm geometry.
    arm_length: float = 9.0 * INCH_TO_MM
    arm_width: float = 12.0
    arm_thickness: float = 4.0

    # Dovetail geometry.
    dovetail_length: float = 14.0
    dovetail_entry_width: float = 10.0
    dovetail_inner_width: float = 12.0
    dovetail_socket_entry_offset: float = 0.6

    # Metal bolt lock geometry for securing arm-to-hub dovetail joints.
    lock_bolt_from_entry: float = 6.0
    lock_bolt_clearance_diameter: float = 3.4
    lock_head_diameter: float = 6.4
    lock_head_depth: float = 1
    lock_nut_flat: float = 5.8
    lock_nut_thickness: float = 2.8

    @property
    def recess_length(self) -> float:
        return self.pcb_length + (2.0 * self.recess_xy_clearance)

    @property
    def recess_width(self) -> float:
        return self.pcb_width + (2.0 * self.recess_xy_clearance)

    @property
    def recess_depth(self) -> float:
        return self.pcb_thickness + self.recess_z_clearance

    @property
    def pcb_hole_offset_x(self) -> float:
        return self.pcb_mount_hole_pitch_x / 2.0

    @property
    def pcb_hole_offset_y(self) -> float:
        return self.pcb_mount_hole_pitch_y / 2.0

    @property
    def battery_holder_hole_offset_x(self) -> float:
        return self.battery_holder_mount_pitch_x / 2.0

    @property
    def battery_holder_hole_offset_y(self) -> float:
        return self.battery_holder_mount_pitch_y / 2.0

    @property
    def battery_holder_center_y(self) -> float:
        return self.battery_holder_center_offset_y

    @property
    def battery_holder_nut_vertex_diameter(self) -> float:
        return (2.0 * self.battery_holder_nut_flat) / math.sqrt(3.0)

    @property
    def dovetail_socket_height(self) -> float:
        return self.arm_thickness + (2.0 * self.dovetail_z_clearance)

    @property
    def hex_radius(self) -> float:
        # Regular-hex circumradius from across-flats value.
        return self.drive_hex_af / math.sqrt(3.0)

    @property
    def hex_leadin_radius(self) -> float:
        return (self.drive_hex_af + self.drive_leadin_delta_af) / math.sqrt(3.0)

    @property
    def lash_hole_radius(self) -> float:
        return (self.hub_outer_diameter / 2.0) - self.lash_hole_radial_inset

    @property
    def arm_lock_bolt_x(self) -> float:
        # Arm local X location, measured inward from the dovetail entry shoulder.
        return -self.lock_bolt_from_entry

    @property
    def hub_lock_bolt_x(self) -> float:
        # World-space X location of the dovetail lock bolt on +X side.
        return (
            (self.hub_outer_diameter / 2.0)
            + self.dovetail_socket_entry_offset
            - self.lock_bolt_from_entry
        )

    @property
    def lock_nut_vertex_diameter(self) -> float:
        # CadQuery polygon() uses vertex-to-vertex diameter for regular polygons.
        return (2.0 * self.lock_nut_flat) / math.sqrt(3.0)


def validate_params(params: HubArmParams) -> None:
    if params.recess_depth >= params.hub_thickness:
        raise ValueError("PCB recess depth must be less than hub thickness.")

    if params.pcb_length <= 0.0 or params.pcb_width <= 0.0:
        raise ValueError("PCB dimensions must be greater than 0.")

    if params.pcb_thickness <= 0.0:
        raise ValueError("PCB thickness must be greater than 0.")

    if params.pcb_mount_hole_pitch_x <= 0.0 or params.pcb_mount_hole_pitch_y <= 0.0:
        raise ValueError("PCB hole pitch must be greater than 0.")

    if params.pcb_mount_hole_diameter <= 0.0:
        raise ValueError("PCB mounting-hole diameter must be greater than 0.")

    if params.pcb_standoff_diameter <= 0.0:
        raise ValueError("PCB standoff diameter must be greater than 0.")

    if params.pcb_standoff_height <= 0.0:
        raise ValueError("PCB standoff height must be greater than 0.")

    if params.pcb_standoff_diameter >= params.pcb_mount_hole_diameter:
        raise ValueError(
            "PCB standoff diameter must be smaller than the hole diameter."
        )

    if params.pcb_mount_hole_pitch_x >= params.pcb_length:
        raise ValueError("PCB hole pitch in X must be less than PCB length.")

    if params.pcb_mount_hole_pitch_y >= params.pcb_width:
        raise ValueError("PCB hole pitch in Y must be less than PCB width.")

    if params.battery_holder_length <= 0.0 or params.battery_holder_width <= 0.0:
        raise ValueError("Battery holder dimensions must be greater than 0.")

    if (
        params.battery_holder_mount_pitch_x <= 0.0
        or params.battery_holder_mount_pitch_y <= 0.0
    ):
        raise ValueError("Battery holder hole pitch must be greater than 0.")

    if params.battery_holder_mount_hole_diameter <= 0.0:
        raise ValueError("Battery holder hole diameter must be greater than 0.")

    if params.battery_holder_mount_pitch_x >= params.battery_holder_length:
        raise ValueError(
            "Battery holder hole pitch in X must be less than battery holder length."
        )

    if params.battery_holder_mount_pitch_y >= params.battery_holder_width:
        raise ValueError(
            "Battery holder hole pitch in Y must be less than battery holder width."
        )

    if not math.isfinite(params.battery_holder_center_offset_y):
        raise ValueError("Battery holder center offset must be finite.")

    if params.battery_holder_nut_flat <= params.battery_holder_mount_hole_diameter:
        raise ValueError("Battery holder nut flat must exceed the screw hole diameter.")

    if params.battery_holder_nut_depth <= 0.0:
        raise ValueError("Battery holder nut depth must be greater than 0.")

    if params.battery_holder_nut_depth >= params.hub_thickness:
        raise ValueError("Battery holder nut depth must be less than hub thickness.")

    min_hub_thickness = (
        params.recess_depth
        + params.recess_floor_thickness
        + params.drive_leadin_depth
        + params.drive_socket_depth
    )
    if params.hub_thickness < min_hub_thickness:
        raise ValueError(
            "Hub thickness must leave the requested solid floor between the "
            "PCB keep-out and the hex drive socket."
        )

    if params.drive_socket_depth >= params.hub_thickness:
        raise ValueError("Drive socket depth must be less than hub thickness.")

    if params.lash_hole_diameter <= 0.0:
        raise ValueError("Lash hole diameter must be greater than 0.")

    if params.lash_hole_count < 2:
        raise ValueError("Lash hole count must be at least 2.")

    if not math.isfinite(params.lash_hole_rotation_deg):
        raise ValueError("Lash hole rotation angle must be finite.")

    if params.lash_hole_radius <= (params.lash_hole_diameter / 2.0):
        raise ValueError(
            "Lash holes are too close to center for the configured diameter."
        )

    if params.arm_length <= params.dovetail_length:
        raise ValueError("Arm length must be longer than dovetail length.")

    if params.dovetail_length <= 0.0:
        raise ValueError("Dovetail length must be greater than 0.")

    if params.dovetail_entry_width <= 0.0 or params.dovetail_inner_width <= 0.0:
        raise ValueError("Dovetail widths must be greater than 0.")

    if params.dovetail_entry_width > params.dovetail_inner_width:
        raise ValueError(
            "Dovetail entry width must be less than or equal to dovetail inner width."
        )

    if params.dovetail_inner_width > params.arm_width:
        raise ValueError(
            "Dovetail inner width must be less than or equal to arm width."
        )

    if not (0.0 < params.lock_bolt_from_entry < params.dovetail_length):
        raise ValueError(
            "Lock-bolt location must be within the dovetail engagement length."
        )

    if params.lock_bolt_clearance_diameter <= 0.0:
        raise ValueError("Lock-bolt clearance diameter must be greater than 0.")

    if params.lock_head_diameter <= params.lock_bolt_clearance_diameter:
        raise ValueError("Lock-bolt head diameter must exceed bolt clearance diameter.")

    if params.lock_head_depth <= 0.0:
        raise ValueError("Lock-bolt head depth must be greater than 0.")

    if params.lock_head_depth >= params.arm_thickness:
        raise ValueError("Lock-bolt head depth must be less than arm thickness.")

    if params.lock_nut_flat <= params.lock_bolt_clearance_diameter:
        raise ValueError("Lock-nut across-flats must exceed bolt clearance diameter.")

    if params.lock_nut_thickness <= 0.0:
        raise ValueError("Lock-nut thickness must be greater than 0.")

    if (params.lock_head_depth + params.lock_nut_thickness) >= params.hub_thickness:
        raise ValueError(
            "Hub thickness must exceed combined lock-head and lock-nut pocket depths."
        )

    min_hub = math.hypot(params.recess_length, params.recess_width) + (
        2.0 * params.hub_wall_margin
    )
    if params.hub_outer_diameter < min_hub:
        raise ValueError(
            f"Hub diameter {params.hub_outer_diameter:.2f} mm is too small. Minimum suggested: {min_hub:.2f} mm."
        )

    pcb_hole_radius = math.hypot(params.pcb_hole_offset_x, params.pcb_hole_offset_y)
    if (pcb_hole_radius + (params.pcb_standoff_diameter / 2.0)) > (
        params.hub_outer_diameter / 2.0
    ):
        raise ValueError("PCB standoffs must fit within the hub diameter.")

    battery_holder_hole_radius = math.hypot(
        params.battery_holder_hole_offset_x, params.battery_holder_hole_offset_y
    )
    if (
        battery_holder_hole_radius + (params.battery_holder_mount_hole_diameter / 2.0)
    ) > (params.hub_outer_diameter / 2.0):
        raise ValueError("Battery holder mounts must fit within the hub diameter.")

    if abs(params.battery_holder_center_y) <= (
        (params.battery_holder_width / 2.0) + params.hex_leadin_radius
    ):
        raise ValueError(
            "Battery holder center offset must clear the hub's hex drive opening."
        )
