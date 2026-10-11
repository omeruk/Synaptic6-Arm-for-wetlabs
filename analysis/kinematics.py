"""Forward / inverse kinematics of the Synaptic6 arm.

Standard DH, PUMA-like layout with a spherical wrist (axes 4, 5, 6 meet at
the wrist centre), so the inverse kinematics has a closed form.

    i   theta   d    a    alpha
    1   q1      d1   0    -90
    2   q2      0    a2    0
    3   q3      0    0    +90
    4   q4      d4   0    -90
    5   q5      0    0    +90
    6   q6      d6   0     0
"""
import numpy as np
from params import Geometry

GEO = Geometry()


def dh(theta, d, a, alpha):
    ct, st, ca, sa = np.cos(theta), np.sin(theta), np.cos(alpha), np.sin(alpha)
    return np.array([[ct, -st * ca, st * sa, a * ct],
                     [st, ct * ca, -ct * sa, a * st],
                     [0, sa, ca, d],
                     [0, 0, 0, 1.0]])


def table(g: Geometry = GEO):
    # (d, a, alpha) per joint
    return [(g.d1, 0, -np.pi / 2), (0, g.a2, 0), (0, 0, np.pi / 2),
            (g.d4, 0, -np.pi / 2), (0, 0, np.pi / 2), (g.d6, 0, 0)]


def frames(q, g: Geometry = GEO):
    """Return the 7 frames T0..T6 (T0 = base)."""
    T = [np.eye(4)]
    for qi, (d, a, al) in zip(q, table(g)):
        T.append(T[-1] @ dh(qi, d, a, al))
    return T


def fk(q, g: Geometry = GEO):
    return frames(q, g)[-1]


def jacobian(q, g: Geometry = GEO):
    """6x6 geometric Jacobian at the TCP, [v; w] = J qdot (base frame)."""
    T = frames(q, g)
    p = T[6][:3, 3]
    J = np.zeros((6, 6))
    for j in range(6):
        z = T[j][:3, 2]
        o = T[j][:3, 3]
        J[:3, j] = np.cross(z, p - o)
        J[3:, j] = z
    return J


def manipulability(q, g: Geometry = GEO):
    """Yoshikawa measure sqrt(det(J J^T)); goes to 0 at a singularity."""
    J = jacobian(q, g)
    return float(np.sqrt(max(np.linalg.det(J @ J.T), 0.0)))


def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def ik(T, g: Geometry = GEO):
    """All closed-form solutions (up to 8) for a target pose T (4x4)."""
    R, p = T[:3, :3], T[:3, 3]
    wc = p - g.d6 * R[:, 2]
    sols = []
    base = np.arctan2(wc[1], wc[0])
    for q1, r_sign in ((base, 1.0), (base + np.pi, -1.0)):
        r = r_sign * np.hypot(wc[0], wc[1])
        z = wc[2] - g.d1
        c = (r * r + z * z - g.a2**2 - g.d4**2) / (2 * g.a2 * g.d4)
        if abs(c) > 1 + 1e-12:
            continue
        for sgn in (1.0, -1.0):
            delta = sgn * np.arccos(np.clip(c, -1, 1))       # elbow, relative
            e = np.arctan2(z, r) - np.arctan2(g.d4 * np.sin(delta),
                                              g.a2 + g.d4 * np.cos(delta))
            q2, q3 = -e, np.pi / 2 - delta
            T03 = np.eye(4)
            for qi, (d, a, al) in zip((q1, q2, q3), table(g)[:3]):
                T03 = T03 @ dh(qi, d, a, al)
            R36 = T03[:3, :3].T @ R
            s5 = np.hypot(R36[0, 2], R36[1, 2])
            for flip in (1.0, -1.0):
                q5 = np.arctan2(flip * s5, R36[2, 2])
                if abs(s5) < 1e-9:       # wrist singularity: pick q4 = 0
                    q4, q6 = 0.0, np.arctan2(R36[1, 0], R36[0, 0])
                else:
                    q4 = np.arctan2(flip * R36[1, 2], flip * R36[0, 2])
                    q6 = np.arctan2(flip * R36[2, 1], -flip * R36[2, 0])
                sols.append(np.array([_wrap(q1), _wrap(q2), _wrap(q3),
                                      _wrap(q4), q5, _wrap(q6)]))
    return sols


def within_limits(q, qmin, qmax):
    return bool(np.all(q >= qmin - 1e-9) and np.all(q <= qmax + 1e-9))
