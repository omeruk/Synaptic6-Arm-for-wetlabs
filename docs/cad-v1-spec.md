# CAD V1 spec (coarse model)

Goal of V1: a complete arm with simple shapes, so kinematics and masses can be
checked before spending time on details. Skeleton conventions are in `skeleton.md`.

## Rules
- One design, top-down: every part is built from the skeleton sketch.
- Dimensions come from the parameters `d1`, `a2`, `d4`, `d6`. Never type them again.
- Each part is its own component, named as in the table below.
- Save a version after every finished part.

## Parts

| # | Component | Shape in V1 | Key dimensions / constraints |
|---|---|---|---|
| 0 | `base` | cylinder plate | Ø140 x 10 mm to start, bolt holes later. J1 actuator mounts vertically on it |
| 1 | `J1_actuator` | STEP from CubeMars (AKE80-8) | listed as Ø87 x 32 mm, check the STEP |
| 2 | `turret` | box / cylinder | joins J1 output to the J2 axis, J2 axis at z = d1 = 120 mm above the base plate |
| 3 | `J2_actuator` | STEP (AKE80-8) | axis +y at the shoulder |
| 4 | `upper_arm` | hollow tube / box | shoulder axis to elbow axis = a2 = 200 mm, centre to centre |
| 5 | `J3_actuator` | STEP (AKE60-8) | axis +y at the elbow, take the dimensions from the STEP |
| 6 | `forearm` | hollow tube | elbow to wrist centre = d4 = 180 mm, J4 (roll) axis along it |
| 7 | `J4_actuator` | STEP (Dynamixel XM430-W350) | roll axis along the forearm |
| 8 | `wrist` | small block | J5 and J6 axes meet at ONE point (wrist centre) |
| 9 | `J5_actuator`, `J6_actuator` | STEP (XM430 / XL430) | J5 axis +y, J6 axis +z at q = 0 |
| 10 | `flange` | disc | face of the tool, TCP is d6 = 100 mm past the wrist centre on the J6 axis |
| 11 | `tool_dummy` | block | 0.2 kg gripper stand-in, so the mass model matches |

## Checks before calling V1 done
1. Measure the distances between joint axes: 120 / 200 / 180 / 100 mm.
2. J4, J5, J6 axes intersect at one point (measure it, don't trust the sketch).
3. Joint limits from `skeleton.md` are possible without collisions (Motion Study).
4. Every part has a material, and the mass from Physical Properties is written down.
5. Fill the table below and send it, so `analysis/params.py` gets real numbers.

## Real masses (fill in from Fusion)

| Item | Model assumption (kg) | CAD (kg) |
|---|---|---|
| upper arm structure | 0.12 | |
| forearm structure | 0.10 | |
| J2 actuator (AKE80-8) | 0.57 | |
| J3 actuator (AKE60-8) | 0.26 | |
| J4 / J5 actuator (XM430) | 0.082 each | |
| J6 actuator (XL430) | 0.057 | |
| flange + gripper stand-in | 0.20 | |
| turret, wrist block | not modelled yet | |

The turret and the wrist block are missing from the mass model, so V1 will probably
show a bit more load than the current numbers. That is expected and the reason for this step.
