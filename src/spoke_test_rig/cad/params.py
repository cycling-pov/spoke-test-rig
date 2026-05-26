from __future__ import annotations

from dataclasses import dataclass
import math


INCH_TO_MM = 25.4
QUARTER_INCH_MM = 0.25 * INCH_TO_MM


@dataclass(frozen=True)
class HubArmParams:
    # Breadboard nominal dimensions.
    breadboard_length: float = 84.5
    breadboard_width: float = 56.5
    breadboard_height: float = 8.5

    # Assembly-fit clearances tuned for PLA/PETG FDM.
    recess_xy_clearance: float = 0.5
    recess_z_clearance: float = 0.4
    recess_floor_thickness: float = 3.0
    dovetail_xy_clearance: float = 0.25
    dovetail_z_clearance: float = 0.2

    # Hub geometry.
    hub_thickness: float = 25.0
    hub_outer_diameter: float = 130.0
    hub_wall_margin: float = 10.0

    # Bottom drive socket geometry.
    drive_hex_af: float = QUARTER_INCH_MM
    drive_socket_depth: float = 8.0
    drive_leadin_depth: float = 1.2
    drive_leadin_delta_af: float = 0.8
    drive_reinforcement_boss_diameter: float = 24.0
    drive_reinforcement_boss_height: float = 3.0

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
    dovetail_inner_width: float = 14.0
    dovetail_socket_entry_offset: float = 0.6

    # Metal bolt lock geometry for securing arm-to-hub dovetail joints.
    lock_bolt_from_entry: float = 6.0
    lock_bolt_clearance_diameter: float = 3.4
    lock_head_diameter: float = 6.4
    lock_head_depth: float = 2.8
    lock_nut_flat: float = 5.8
    lock_nut_thickness: float = 2.8

    @property
    def recess_length(self) -> float:
        return self.breadboard_length + (2.0 * self.recess_xy_clearance)

    @property
    def recess_width(self) -> float:
        return self.breadboard_width + (2.0 * self.recess_xy_clearance)

    @property
    def recess_depth(self) -> float:
        return self.breadboard_height + self.recess_z_clearance

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
        raise ValueError("Breadboard recess depth must be less than hub thickness.")

    min_hub_thickness = (
        params.recess_depth
        + params.recess_floor_thickness
        + params.drive_reinforcement_boss_height
        + params.drive_leadin_depth
        + params.drive_socket_depth
    )
    if params.hub_thickness < min_hub_thickness:
        raise ValueError(
            "Hub thickness must leave the requested solid floor between the "
            "breadboard recess and the hex drive socket."
        )

    if params.drive_socket_depth >= params.hub_thickness:
        raise ValueError("Drive socket depth must be less than hub thickness.")

    if params.drive_reinforcement_boss_height <= 0.0:
        raise ValueError("Drive reinforcement boss height must be greater than 0.")

    if params.drive_reinforcement_boss_diameter <= params.drive_hex_af:
        raise ValueError("Drive reinforcement boss diameter must exceed hex socket AF.")

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
