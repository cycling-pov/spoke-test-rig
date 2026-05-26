from __future__ import annotations

import argparse
import os

from ocp_vscode import set_port, show

from spoke_test_rig.cad.arm import build_arm
from spoke_test_rig.cad.assembly import build_assembly
from spoke_test_rig.cad.hub import build_hub
from spoke_test_rig.cad.params import HubArmParams


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open build123d models in the OCP viewer for interactive inspection."
    )
    parser.add_argument(
        "--model",
        choices=("hub", "arm", "assembly", "all"),
        default="all",
        help="Select which model to show (default: all).",
    )
    args = parser.parse_args()

    params = HubArmParams()
    shapes = []
    names = []

    if args.model in {"hub", "all"}:
        shapes.append(build_hub(params))
        names.append("hub")

    if args.model in {"arm", "all"}:
        shapes.append(build_arm(params))
        names.append("arm")

    if args.model in {"assembly", "all"}:
        shapes.append(build_assembly(params))
        names.append("assembly")

    if not shapes:
        raise SystemExit("No models selected to display.")

    port = int(os.environ.get("OCP_VSCODE_PORT", "3939"))
    set_port(port)
    show(*shapes, names=names, port=port)


if __name__ == "__main__":
    main()
