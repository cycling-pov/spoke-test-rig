# Spoke Test Rig CAD (build123d)

Parametric build123d models for a rotating hub and detachable LED arms.

## What this generates

- Hub with PCB locating posts for a 56 x 47 mm board with 42 mm mounting-hole pitch in both axes.
- Hub backside pilot holes for a 78 x 42 mm dual battery holder with 55.5 x 21.4 mm M3 hole pitch.
- Bottom 1/4-inch hex drive socket for a rotating shank.
- Two radial dovetail receivers at 180 degrees in the hub.
- Separate 9-inch arms with matching male dovetail mounts.
- Through-bolt lock retention at each arm-hub dovetail with arm-side head counterbore and hub-side hex-nut trap.

## Key defaults

- PCB nominal: 56.0 x 47.0 x 1.6 mm
- PCB mounting pattern: 42.0 x 42.0 mm
- PCB locating posts: 3.0 mm diameter x 2.5 mm tall
- Battery holder nominal: 78.0 x 42.0 mm
- Battery holder mounting pattern: 55.5 x 21.4 mm
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

Edit `src/spoke_test_rig/cad/params.py` to adjust PCB fit, clearances, hub size, arm dimensions, or dovetail fit.
