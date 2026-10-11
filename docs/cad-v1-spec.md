# CAD V1 spec (coarse model)

Goal of V1: a complete arm with simple shapes, so kinematics and masses can be
checked before spending time on details. Skeleton conventions are in `skeleton.md`.

## Rules
- One design, top-down: every part is built from the skeleton sketch.
- Dimensions come from the parameters `d1`, `a2`, `d4`, `d6`. Never type them again.
- Each part is its own component, named as in the table below.
- Save a version after every finished part.

## Parts

Sizes and weights are from the CubeMars catalogue; take the exact drawing from the STEP file.

| # | Component | Shape in V1 | Key dimensions / constraints |
|---|---|---|---|
| 0 | `base` | cylinder plate | Ø180 x 12 mm to start, bolt holes later. J1 actuator mounts vertically on it, cables go through its bore |
| 1 | `J1_actuator` | STEP: CubeMars **AKH70-48** | Ø90 x 81.5 mm, 1396 g, hollow bore 7 mm, axis +z |
| 2 | `turret` | box / cylinder | joins the J1 output to the J2 axis, J2 axis at z = d1 = 200 mm above the base plate |
| 3 | `J2_actuator` | STEP: **AKH70-48** | Ø90 x 81.5 mm, axis +y at the shoulder |
| 4 | `upper_arm` | hollow tube / box | shoulder axis to elbow axis = a2 = 290 mm, centre to centre |
| 5 | `J3_actuator` | STEP: CubeMars **AKH70-16** | Ø90 x 60.5 mm, 879 g, axis +y at the elbow |
| 6 | `forearm` | hollow tube | elbow to wrist centre = d4 = 290 mm, J4 (roll) axis along it |
| 7 | `J4_actuator` | STEP: CubeMars **AK45-36 V3** | Ø55 x 56.5 mm, 349 g, roll axis along the forearm |
| 8 | `wrist` | small block | J5 and J6 axes meet at ONE point (wrist centre) |
| 9 | `J5_actuator`, `J6_actuator` | STEP: **AK45-36 V3** | J5 axis +y, J6 axis +z at q = 0 |
| 10 | `flange` | disc | face of the tool, TCP is d6 = 120 mm past the wrist centre on the J6 axis |
| 11 | `tool_dummy` | block | 0.5 kg gripper stand-in, so the mass model matches (payload 2 kg on top) |

All six modules have the driver inside and talk CAN, so there is one bus and one protocol for the whole arm.

## Checks before calling V1 done
1. Measure the distances between joint axes: 120 / 200 / 180 / 100 mm.
2. J4, J5, J6 axes intersect at one point (measure it, don't trust the sketch).
3. Joint limits from `skeleton.md` are possible without collisions (Motion Study).
4. Every part has a material, and the mass from Physical Properties is written down.
5. Fill the table below and send it, so `analysis/params.py` gets real numbers.

## Real masses (fill in from Fusion)

| Item | Model assumption (kg) | CAD (kg) |
|---|---|---|
| upper arm structure | 0.45 | |
| forearm structure | 0.35 | |
| J2 actuator (AKH70-48) | 1.396 | |
| J3 actuator (AKH70-16) | 0.879 | |
| J4 / J5 / J6 actuator (AK45-36 V3) | 0.349 each | |
| flange + gripper stand-in | 0.50 | |
| turret, wrist block | not modelled yet | |

The turret and the wrist block are missing from the mass model, so V1 will probably
show a bit more load than the current numbers. That is expected and the reason for this step.

## Open questions to settle with the STEP files
- Does the 90 mm AKH70-48 fit at the shoulder with d1 = 200 mm without hitting the base?
- Is the 7 mm bore enough for the power and CAN cables of the whole arm?
- Voltage: check that all three module types can share one supply.
