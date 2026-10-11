# Synaptic6 – Arm for wetlabs

A 6-axis robot arm I'm designing for wet lab work (moving tubes and plates, and later pipetting). It's a CAD and simulation project. I'm not building the hardware, so everything here is design, calculation and sim.

**Status:** work in progress. Checked boxes are done.

- [x] Requirements and first torque estimate
- [x] Actuator choice (CubeMars AK series for the big joints)
- [ ] Skeleton + full assembly in Fusion 360
- [ ] Forward / inverse kinematics, workspace map
- [ ] Link stress and deflection (Fusion simulation)
- [ ] URDF + simulation (MuJoCo or PyBullet)
- [ ] AprilTag visual servoing in sim
- [ ] Swappable end effectors (tool changer)

## Why this exists

I wanted a project that covers the whole chain: mechanical design, motor selection, kinematics, vision and simulation. Wet labs are a good target because the arm works near people, carries light loads, and needs repeatable positioning more than raw strength.

## Design targets (first guess, will change)

| | |
|---|---|
| Reach | ~400 mm |
| Payload | 0.5 kg incl. gripper |
| Repeatability goal | ≲ 0.5 mm, fixed up with camera feedback |
| Actuators | J1–J3: CubeMars AK60-6 / AK70-10, J4–J6: small light actuators |
| Sensing | Camera on the wrist + AprilTags on the workspace and tools |

## Actuator notes

CubeMars AK actuators are quasi-direct-drive: low gear ratio, backdrivable, CAN bus. Good for safety and torque control. Downsides I have to deal with:

- Most versions have no brake, so the arm drops when power is cut. Shoulder needs a brake or a mechanical lock.
- Backlash and encoder resolution are not enough for pipetting on their own, hence the camera feedback.
- They are heavy (~0.5 kg), so the wrist can't use them.

(Numbers come from memory of the datasheets. I still need to check them before finalising.)

## Torque estimate

`analysis/torque.py` computes the static torque at the shoulder and elbow with the arm fully stretched out horizontally (worst case), times a 1.5 safety factor. With the current assumptions:

| Joint | Static | With 1.5x margin + acceleration |
|---|---|---|
| J2 shoulder | 5.4 Nm | ~9.5 Nm |
| J3 elbow | 2.2 Nm | ~3.3 Nm |

The result is very sensitive to the elbow actuator mass, so lighter elbow = much lower shoulder load.

## Idea for later: swappable end effectors

A standard flange (magnets + alignment pins, a few pogo pins for power/data) with an AprilTag on each tool and on its dock. The arm finds the dock with its camera, the pins correct the last millimetre. Tools: gripper, tube/plate gripper, pipette, sensor.

## Repo layout

```
analysis/   calculations (torque, later kinematics and error budget)
cad/        Fusion 360 files, STEP, renders
urdf/       robot description
sim/        simulation scenes
docs/       design notes and decisions
```

## Running

```
python analysis/torque.py
```
No dependencies yet.
