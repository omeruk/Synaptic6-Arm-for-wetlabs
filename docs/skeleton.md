# Skeleton and kinematic conventions

This is the reference for the CAD. If the Fusion model disagrees with this page,
one of them is wrong and I fix it before building more on top.

## Dimensions (parameters, all in `analysis/params.py`)

| Name | Meaning | Value |
|---|---|---|
| d1 | base plate -> shoulder axis (J2) | 120 mm |
| a2 | shoulder -> elbow (upper arm) | 200 mm |
| d4 | elbow -> wrist centre (forearm) | 180 mm |
| d6 | wrist centre -> flange / TCP | 100 mm |

Max reach from the shoulder: a2 + d4 + d6 = 480 mm.

## Zero pose and joint axes

At q = 0 the upper arm points along +x, the forearm and the tool point up (+z).

| Joint | Axis at q = 0 | Located at | Role |
|---|---|---|---|
| J1 | +z | base | base rotation |
| J2 | +y | shoulder (0, 0, d1) | shoulder pitch |
| J3 | +y | elbow (a2, 0, d1) | elbow pitch |
| J4 | +z | elbow, along forearm | forearm roll |
| J5 | +y | wrist centre (a2, 0, d1+d4) | wrist pitch |
| J6 | +z | wrist centre | tool roll |

J4, J5, J6 meet at one point (wrist centre). That is what gives the closed-form IK.

## DH table (standard convention)

| i | theta | d | a | alpha |
|---|---|---|---|---|
| 1 | q1 | d1 | 0 | -90° |
| 2 | q2 | 0 | a2 | 0 |
| 3 | q3 | 0 | 0 | +90° |
| 4 | q4 | d4 | 0 | -90° |
| 5 | q5 | 0 | 0 | +90° |
| 6 | q6 | d6 | 0 | 0 |

Frame 6 sits at the TCP (it already includes d6).

Stretched-out reference pose: q = [0, 0, 90°, 0, 0, 0] puts the TCP at x = 480 mm, z = 120 mm, tool horizontal.

## Joint limits used in the analysis (assumed)

| J1 | J2 | J3 | J4 | J5 | J6 |
|---|---|---|---|---|---|
| ±170° | -120° .. +30° | ±135° | ±170° | ±115° | ±170° |

The 170° limits on the roll joints are on purpose, so cables can't wind up.

## Fusion 360 axes

Fusion defaults to Y-up. `cad/fusion_skeleton.py` draws the side view on the XY
plane, so Fusion's Y is the arm's z (up). Keep that in mind when exporting a URDF,
which wants z up.
