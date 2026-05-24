from __future__ import annotations

from dataclasses import dataclass
import math


INCH_TO_MM = 25.4
QUARTER_INCH_MM = 0.25 * INCH_TO_MM


@dataclass(frozen=True)
class HubArmParams:
    # Breadboard nominal dimensions.
    breadboard_length: float = 83.5
    breadboard_width: float = 55.5
    breadboard_height: float = 8.5

    # Assembly-fit clearances tuned for PLA/PETG FDM.
    recess_xy_clearance: float = 0.5
    recess_z_clearance: float = 0.4
    dovetail_xy_clearance: float = 0.25
    dovetail_z_clearance: float = 0.2

    # Hub geometry.
    hub_thickness: float = 15.0
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
    arm_width: float = 16.0
    arm_thickness: float = 4.0

    # Dovetail geometry.
    dovetail_length: float = 14.0
    dovetail_entry_width: float = 10.0
    dovetail_inner_width: float = 14.0
    dovetail_socket_entry_offset: float = 0.6

    # Lock pin geometry for securing arm-to-hub dovetail joints.
    pin_hole_from_entry: float = 6.0
    pin_hole_top_diameter: float = 3.6
    pin_hole_bottom_diameter: float = 3.3
    pin_top_diameter: float = 3.35
    pin_bottom_diameter: float = 3.1
    pin_length: float = 17.0

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
    def arm_pin_hole_x(self) -> float:
        # Arm local X location, measured inward from the dovetail entry shoulder.
        return -self.pin_hole_from_entry

    @property
    def hub_pin_hole_x(self) -> float:
        # World-space X location of the dovetail lock pin on +X side.
        return (
            (self.hub_outer_diameter / 2.0)
            + self.dovetail_socket_entry_offset
            - self.pin_hole_from_entry
        )


def validate_params(params: HubArmParams) -> None:
    if params.recess_depth >= params.hub_thickness:
        raise ValueError("Breadboard recess depth must be less than hub thickness.")

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

    if not (0.0 < params.pin_hole_from_entry < params.dovetail_length):
        raise ValueError(
            "Pin-hole location must be within the dovetail engagement length."
        )

    if params.pin_hole_top_diameter <= params.pin_hole_bottom_diameter:
        raise ValueError("Pin-hole top diameter must exceed bottom diameter.")

    if params.pin_bottom_diameter <= 0.0 or params.pin_top_diameter <= 0.0:
        raise ValueError("Pin diameters must be greater than 0.")

    if params.pin_top_diameter <= params.pin_bottom_diameter:
        raise ValueError("Pin top diameter must exceed pin bottom diameter.")

    if params.pin_length <= params.hub_thickness:
        raise ValueError("Pin length should exceed hub thickness for retention.")

    if params.pin_top_diameter >= params.pin_hole_top_diameter:
        raise ValueError("Pin top diameter must be smaller than hole top diameter.")

    if params.pin_bottom_diameter >= params.pin_hole_bottom_diameter:
        raise ValueError(
            "Pin bottom diameter must be smaller than hole bottom diameter."
        )

    min_hub = math.hypot(params.recess_length, params.recess_width) + (
        2.0 * params.hub_wall_margin
    )
    if params.hub_outer_diameter < min_hub:
        raise ValueError(
            f"Hub diameter {params.hub_outer_diameter:.2f} mm is too small. Minimum suggested: {min_hub:.2f} mm."
        )
