# Spoke Test Rig CAD (CadQuery)

Parametric CadQuery models for a rotating hub and detachable LED arms.

## What this generates

- Hub with top recess sized for a standard 400-point mini breadboard.
- Bottom 1/4-inch hex drive socket for a rotating shank.
- Two radial dovetail receivers at 180 degrees in the hub.
- Separate 9-inch arms with matching male dovetail mounts.

## Key defaults

- Breadboard nominal: 83.5 x 55.5 x 8.5 mm
- Recess fit: slip-fit (+0.5 mm XY, +0.4 mm depth)
- Hub thickness: 15 mm
- Arms: 228.6 mm long (9 in), 16 x 4 mm section
- Dovetail: radial slide-in, friction fit
- Material tuning: PLA FDM

## Export models

```bash
uv run export
```

Outputs are written to `exports/`

## Tune dimensions

Edit `src/spoke_test_rig/cad/params.py` to adjust clearances, hub size, arm dimensions, or dovetail fit.
