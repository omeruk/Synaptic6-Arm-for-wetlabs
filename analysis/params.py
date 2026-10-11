"""Single source of truth for the arm geometry, masses and limits.

Lengths in m, masses in kg, angles in rad. Everything here is a design
assumption until the CAD gives real numbers. Change it here and every
analysis script follows.
"""
from dataclasses import dataclass, field
import numpy as np

G = 9.81


@dataclass(frozen=True)
class Geometry:
    d1: float = 0.20    # base plate -> shoulder axis (J2)
    a2: float = 0.29    # shoulder -> elbow (upper arm)
    d4: float = 0.29    # elbow -> wrist centre (forearm)
    d6: float = 0.12    # wrist centre -> flange / TCP


# Joint limits (q as defined by the DH table in kinematics.py).
# Zero pose: upper arm horizontal (+x), forearm and tool pointing up (+z).
Q_MIN = np.radians([-170, -120, -135, -170, -115, -170])
Q_MAX = np.radians([170, 30, 135, 170, 115, 170])


@dataclass(frozen=True)
class Component:
    """A lumped mass rigidly attached to a DH frame (moves with q1..q_frame)."""
    name: str
    frame: int          # 1..6, the frame it is attached to
    local: tuple        # position in that frame (m)
    mass: float         # kg


DEFAULT_ACT_MASS = {2: 0.52, 3: 0.29, 4: 0.082, 5: 0.082, 6: 0.057}


PAYLOAD = 2.0   # kg carried at the TCP
TOOL = 0.5      # kg gripper / end effector


def build_components(g: Geometry = Geometry(), payload: float = PAYLOAD,
                     tool: float = TOOL, structure_scale: float = 1.0,
                     act_mass: dict = None) -> list:
    """Mass model. act_mass[j] = mass of the actuator that drives joint j.
    Default actuator masses are datasheet numbers from memory (verify).
    The J1 actuator sits in the fixed base, so it is not a moving mass."""
    s = structure_scale
    m = {**DEFAULT_ACT_MASS, **(act_mass or {})}
    return [
        # frame 1 rotates with J1 only: carries the J2 actuator body
        Component("J2 actuator", 1, (0, 0, 0), m[2]),
        # frame 2 (origin at elbow) carries upper arm + J3 actuator body
        Component("upper arm structure", 2, (-g.a2 / 2, 0, 0), 0.45 * s),
        Component("J3 actuator", 2, (0, 0, 0), m[3]),
        # frame 3 (origin at elbow, z along forearm) carries forearm + J4 body
        Component("forearm structure", 3, (0, 0, g.d4 / 2), 0.35 * s),
        Component("J4 actuator", 3, (0, 0, 0.75 * g.d4), m[4]),
        # frame 4 (origin at wrist centre) carries J5 body
        Component("J5 actuator", 4, (0, 0, 0), m[5]),
        # frame 5 carries J6 body
        Component("J6 actuator", 5, (0, 0, 0), m[6]),
        # frame 6 origin IS the TCP (it already includes d6), so the gripper
        # sits half way back towards the wrist centre and the payload at 0
        Component("tool + gripper", 6, (0, 0, -g.d6 * 0.5), tool),
        Component("payload", 6, (0, 0, 0), payload),
    ]
