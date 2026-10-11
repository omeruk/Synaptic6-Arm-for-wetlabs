"""Gravity torque, mass matrix and worst-case search for the lumped-mass model.

Every component is a point mass attached to a DH frame. For a point p on
frame k the position Jacobian column of joint j (j <= k) is z_{j-1} x (p - o_{j-1}).
Gravity torque is tau = sum m * Jv^T * (0,0,g)  (sign: torque the joint must supply
to hold the arm still). The mass matrix ignores link rotational inertia and
Coriolis terms; both are small for these masses and speeds.
"""
import numpy as np
from params import G, Geometry, Q_MIN, Q_MAX, build_components
import kinematics as kin


def _points(q, comps, g):
    T = kin.frames(q, g)
    pts = []
    for c in comps:
        Tk = T[c.frame]
        p = Tk[:3, :3] @ np.array(c.local) + Tk[:3, 3]
        pts.append((c, p))
    return T, pts


def _jv(T, p, frame):
    J = np.zeros((3, 6))
    for j in range(frame):
        J[:, j] = np.cross(T[j][:3, 2], p - T[j][:3, 3])
    return J


def gravity_torque(q, comps=None, g: Geometry = None):
    g = g or kin.GEO
    comps = comps or build_components(g)
    T, pts = _points(q, comps, g)
    tau = np.zeros(6)
    for c, p in pts:
        tau += c.mass * _jv(T, p, c.frame).T @ np.array([0, 0, G])
    return tau


def potential_energy(q, comps=None, g: Geometry = None):
    g = g or kin.GEO
    comps = comps or build_components(g)
    _, pts = _points(q, comps, g)
    return sum(c.mass * G * p[2] for c, p in pts)


def mass_matrix(q, comps=None, g: Geometry = None):
    g = g or kin.GEO
    comps = comps or build_components(g)
    T, pts = _points(q, comps, g)
    M = np.zeros((6, 6))
    for c, p in pts:
        Jv = _jv(T, p, c.frame)
        M += c.mass * Jv.T @ Jv
    return M


def total_mass(comps=None):
    comps = comps or build_components()
    return sum(c.mass for c in comps)


def worst_case(n=200_000, seed=1, alpha=5.0, comps=None, g: Geometry = None,
               qmin=Q_MIN, qmax=Q_MAX):
    """Random search over the joint space. Returns per-joint worst static
    torque, worst static+dynamic torque (alpha rad/s^2 on every joint) and
    the configuration that produced it."""
    g = g or kin.GEO
    comps = comps or build_components(g)
    rng = np.random.default_rng(seed)
    # the stretched-out horizontal pose is added by hand so the search can
    # never miss the obvious worst case
    qs = np.vstack([[0, 0, np.pi / 2, 0, 0, 0], rng.uniform(qmin, qmax, size=(n, 6))])
    st = np.zeros(6); sd = np.zeros(6)
    st_q = [qs[0]] * 6

    def score(q):
        tau = np.abs(gravity_torque(q, comps, g))
        return tau, tau + np.abs(mass_matrix(q, comps, g)) @ np.full(6, alpha)

    for q in qs:
        tau, tau_dyn = score(q)
        for j in range(6):
            if tau[j] > st[j]:
                st[j], st_q[j] = tau[j], q
            sd[j] = max(sd[j], tau_dyn[j])
    # local refinement: small random steps around the best pose of each joint
    for j in range(6):
        q = st_q[j]
        for _ in range(300):
            cand = np.clip(q + rng.normal(scale=0.05, size=6), qmin, qmax)
            tau, tau_dyn = score(cand)
            sd[j] = max(sd[j], tau_dyn[j])
            if tau[j] > st[j]:
                st[j], q = tau[j], cand
        st_q[j] = q
    return st, sd, st_q
