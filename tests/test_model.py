import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "analysis"))
import numpy as np
import kinematics as kin
import dynamics as dyn
from params import G, Geometry, Component, build_components, Q_MIN, Q_MAX

rng = np.random.default_rng(42)


def rand_q():
    return rng.uniform(Q_MIN, Q_MAX)


def test_zero_pose_position():
    T = kin.fk(np.zeros(6))
    g = kin.GEO
    assert np.allclose(T[:3, 3], [g.a2, 0, g.d1 + g.d4 + g.d6])


def test_extended_pose_reach():
    T = kin.fk([0, 0, np.pi / 2, 0, 0, 0])
    g = kin.GEO
    assert np.isclose(T[0, 3], g.a2 + g.d4 + g.d6)
    assert np.isclose(T[2, 3], g.d1)


def test_ik_roundtrip():
    for _ in range(500):
        q = rng.uniform(-np.pi, np.pi, 6)
        q[4] = rng.uniform(0.05, np.pi - 0.05) * rng.choice([-1, 1])
        T = kin.fk(q)
        sols = kin.ik(T)
        assert len(sols) == 8
        assert all(np.abs(kin.fk(s) - T).max() < 1e-8 for s in sols)


def test_jacobian_matches_finite_difference():
    for _ in range(50):
        q = rand_q()
        J = kin.jacobian(q)
        eps = 1e-6
        for j in range(6):
            dq = np.zeros(6); dq[j] = eps
            dp = (kin.fk(q + dq)[:3, 3] - kin.fk(q - dq)[:3, 3]) / (2 * eps)
            assert np.allclose(J[:3, j], dp, atol=1e-6)


def test_gravity_torque_is_gradient_of_potential_energy():
    comps = build_components()
    for _ in range(50):
        q = rand_q()
        tau = dyn.gravity_torque(q, comps)
        eps = 1e-6
        for j in range(6):
            dq = np.zeros(6); dq[j] = eps
            dU = (dyn.potential_energy(q + dq, comps) - dyn.potential_energy(q - dq, comps)) / (2 * eps)
            assert np.isclose(tau[j], dU, atol=1e-6)


def test_gravity_torque_matches_hand_calc_extended_pose():
    """Arm stretched out horizontally: compare with the closed form."""
    g = kin.GEO
    comps = build_components(g)
    q = np.array([0, 0, np.pi / 2, 0, 0, 0])
    tau = dyn.gravity_torque(q, comps)
    by = {c.name: c for c in comps}
    # horizontal distances from the shoulder (J2) axis
    x = {"J2 actuator": 0,
         "upper arm structure": g.a2 / 2,
         "J3 actuator": g.a2,
         "forearm structure": g.a2 + g.d4 * 0.5,
         "J4 actuator": g.a2 + 0.75 * g.d4,
         "J5 actuator": g.a2 + g.d4,
         "J6 actuator": g.a2 + g.d4,
         "tool + gripper": g.a2 + g.d4 + g.d6 * 0.5,
         "payload": g.a2 + g.d4 + g.d6}
    expected_j2 = sum(by[k].mass * G * v for k, v in x.items())
    assert np.isclose(abs(tau[1]), expected_j2, rtol=1e-9)
    # J3 only sees what is beyond the elbow
    expected_j3 = sum(by[k].mass * G * (v - g.a2) for k, v in x.items() if v >= g.a2)
    assert np.isclose(abs(tau[2]), expected_j3, rtol=1e-9)
    assert abs(tau[0]) < 1e-9  # base rotation holds nothing against gravity


def test_mass_matrix_symmetric_positive_definite():
    for _ in range(50):
        M = dyn.mass_matrix(rand_q())
        assert np.allclose(M, M.T)
        assert np.all(np.linalg.eigvalsh(M) > -1e-12)


def test_kinetic_energy_consistency():
    """qdot^T M qdot must equal sum 1/2 m v^2 computed from FK velocities."""
    comps = build_components()
    q = rand_q(); qd = rng.normal(size=6)
    eps = 1e-6
    ke = 0.0
    T, pts = dyn._points(q, comps, kin.GEO)
    Tn, ptsn = dyn._points(q + eps * qd, comps, kin.GEO)
    for (c, p), (_, pn) in zip(pts, ptsn):
        v = (pn - p) / eps
        ke += 0.5 * c.mass * v @ v
    assert np.isclose(ke, 0.5 * qd @ dyn.mass_matrix(q, comps) @ qd, rtol=1e-4)


def test_backlash_error_stretched_pose():
    """9 arcmin at the shoulder, arm stretched out: error = angle x distance."""
    import error_budget as eb
    b = np.array([0, 9, 0, 0, 0, 0], dtype=float)
    e = eb.tip_error(b, [np.array([0, 0, np.pi / 2, 0, 0, 0])])
    g = kin.GEO
    dist = g.a2 + g.d4 + g.d6          # shoulder axis to TCP, all in a line
    assert np.isclose(e[0, 1], 9 * eb.ARCMIN * dist * 1e3, rtol=1e-9)
    assert np.isclose(e[0, 1], 1.2566, atol=1e-3)
