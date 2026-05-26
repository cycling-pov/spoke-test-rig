# Spoke Test Rig CAD (build123d)

Parametric build123d models for a rotating hub and detachable LED arms.

## What this generates

- Hub with top recess sized for a standard 400-point mini breadboard.
- Bottom 1/4-inch hex drive socket for a rotating shank.
- Two radial dovetail receivers at 180 degrees in the hub.
- Separate 9-inch arms with matching male dovetail mounts.
- Through-bolt lock retention at each arm-hub dovetail with arm-side head counterbore and hub-side hex-nut trap.

## Key defaults

- Breadboard nominal: 83.5 x 55.5 x 8.5 mm
- Recess fit: slip-fit (+0.5 mm XY, +0.4 mm depth)
- Hub thickness: 25 mm
- Arms: 228.6 mm long (9 in), 12 x 4 mm section
- Dovetail: radial slide-in with M3-class through-bolt retention
- Material tuning: PLA FDM

## Export models

```bash
uv run export
```

Outputs are written to `exports/`

## Visualize models in OCP viewer

The project includes the OCP VS Code viewer integration. Launch the viewer script with:

```bash
uv run view
```

Optional model filter:

```bash
uv run view --model hub
uv run view --model arm
uv run view --model assembly
```

## Tune dimensions

Edit `src/spoke_test_rig/cad/params.py` to adjust clearances, hub size, arm dimensions, or dovetail fit.
