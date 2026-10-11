# Design notes

## Why 6 axes with a spherical wrist
Putting the J4, J5, J6 axes through one point gives a closed-form inverse kinematics solution and keeps the wrist motion easy to reason about.

## Why CubeMars for J1–J3
Torque density and CAN bus in one package, backdrivable so it's safer around people. Wrist uses lighter actuators because heavy motors at the end of the arm load the shoulder a lot.

## Open problems
- Brake / lock for the shoulder (power loss with liquids in the gripper).
- Pipetting accuracy: actuator backlash is too large alone, needs camera feedback.
- Cable routing and joint limits (no endless rotation, avoid wrapping cables).
- Surfaces must be wipeable with ethanol, no open pockets.

## Next
1. Parametric skeleton in Fusion 360 (L2, L3, LW as parameters).
2. Real masses from CAD back into torque.py.
3. Kinematics + workspace plot.
