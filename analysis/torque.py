"""Worst-case static torque for the shoulder (J2) and elbow (J3).

Arm fully extended and horizontal. Lengths in m, masses in kg.
All numbers are first guesses, change them as the CAD gets real masses.
"""
G = 9.81
SAFETY = 1.5
ALPHA = 5.0  # rad/s^2, joint acceleration used for the dynamic term

L2, L3, LW = 0.18, 0.17, 0.05  # shoulder->elbow, elbow->wrist, wrist->tip

payload = 0.5
gripper = 0.2
m_upper = 0.25
m_fore = 0.20
m_wrist = 0.30          # three small wrist actuators
m_elbow_motor = 0.50    # check the datasheet


def elbow_torque():
    tip = payload + gripper
    return (m_fore * G * L3 / 2
            + m_wrist * G * L3
            + tip * G * (L3 + LW))


def shoulder_torque():
    tip = payload + gripper
    return (m_upper * G * L2 / 2
            + m_elbow_motor * G * L2
            + m_fore * G * (L2 + L3 / 2)
            + m_wrist * G * (L2 + L3)
            + tip * G * (L2 + L3 + LW))


def shoulder_inertia():
    tip = payload + gripper
    return (m_upper * L2**2 / 3
            + m_elbow_motor * L2**2
            + m_fore * (L2**2 + L2 * L3 + L3**2 / 3)
            + m_wrist * (L2 + L3)**2
            + tip * (L2 + L3 + LW)**2)


if __name__ == "__main__":
    t2, t3 = shoulder_torque(), elbow_torque()
    dyn = shoulder_inertia() * ALPHA
    print(f"J2 static: {t2:.2f} Nm, J3 static: {t3:.2f} Nm")
    print(f"J2 with {SAFETY}x margin: {t2 * SAFETY:.2f} Nm")
    print(f"J2 with acceleration ({ALPHA} rad/s^2) and margin: {(t2 + dyn) * SAFETY:.2f} Nm")
    print(f"J3 with {SAFETY}x margin: {t3 * SAFETY:.2f} Nm")
