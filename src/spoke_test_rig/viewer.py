from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap


def _build_preview_script(model: str) -> str:
    show_hub = model in {"hub", "all"}
    show_arm = model in {"arm", "all"}
    show_assembly = model in {"assembly", "all"}

    return (
        textwrap.dedent(
            f"""
        from spoke_test_rig.cad.arm import build_arm
        from spoke_test_rig.cad.assembly import build_assembly
        from spoke_test_rig.cad.hub import build_hub
        from spoke_test_rig.cad.params import HubArmParams

        params = HubArmParams()

        if {show_hub}:
            show_object(build_hub(params), name="hub")

        if {show_arm}:
            show_object(build_arm(params), name="arm")

        if {show_assembly}:
            assembly = build_assembly(params)
            show_object(assembly.toCompound(), name="assembly")
        """
        ).strip()
        + "\n"
    )


def _find_viewer_command() -> str | None:
    for command in ("cq-editor", "cq-editor.exe"):
        if shutil.which(command):
            return command
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open CadQuery models in CQ-editor for interactive inspection."
    )
    parser.add_argument(
        "--model",
        choices=("hub", "arm", "assembly", "all"),
        default="all",
        help="Select which model to show (default: all).",
    )
    args = parser.parse_args()

    command = _find_viewer_command()
    if command is None:
        raise SystemExit(
            "Could not find `cq-editor` on PATH. Run `uv sync` to install project dependencies, then rerun `uv run view`."
        )

    package_root = Path(__file__).resolve().parents[2]
    src_root = package_root / "src"

    env = os.environ.copy()
    existing_path = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(src_root) if not existing_path else f"{src_root}{os.pathsep}{existing_path}"
    )

    script_text = _build_preview_script(args.model)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(script_text)
        script_path = Path(temp_file.name)

    try:
        completed = subprocess.run([command, str(script_path)], env=env, check=False)
        if completed.returncode != 0:
            raise SystemExit(f"CQ-editor exited with code {completed.returncode}.")
    finally:
        script_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
