from __future__ import annotations

import cadquery as cq

from spoke_test_rig.cad.arm import build_arm
from spoke_test_rig.cad.hub import build_hub
from spoke_test_rig.cad.params import HubArmParams


def build_assembly(params: HubArmParams) -> cq.Assembly:
    hub = build_hub(params)
    arm = build_arm(params)

    radius = params.hub_outer_diameter / 2.0
    arm_insert_origin = radius + params.dovetail_socket_entry_offset
    arm_center_z = (params.hub_thickness - params.dovetail_socket_height) / 2.0

    assembly = cq.Assembly(name="hub_with_arms")
    assembly.add(hub, name="hub")

    arm_a = arm.translate((arm_insert_origin, 0.0, arm_center_z))
    arm_b = arm.rotate((0, 0, 0), (0, 0, 1), 180.0).translate(
        (-arm_insert_origin, 0.0, arm_center_z)
    )

    assembly.add(arm_a, name="arm_a")
    assembly.add(arm_b, name="arm_b")

    return assembly
