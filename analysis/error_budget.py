"""How much does gear backlash move the tool tip?

A joint with backlash b (rad) can be off by up to b at the output. That moves
the TCP by J[:3, j] * b, where J is the position Jacobian. The result depends on
the pose, so this samples poses and reports the worst and typical cases.

Backlash is a peak-to-peak range: the joint can sit anywhere inside it, so the
error around the commanded position is up to +/- half of what is printed
if the controller centres on it. The table shows the full range (conservative).

Not included yet: link deflection (needs CAD + FEA), encoder resolution,
calibration, camera noise, thermal drift.
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import kinematics as kin
from params import Q_MIN, Q_MAX
from actuators import ACTUATORS, ASSUMED_BACKLASH_ARCMIN

ARCMIN = np.pi / (180 * 60)


def backlash_arcmin(choice):
    """choice: {joint number: actuator name}. J1 is not in the moving-mass
    selection, so it defaults to the same part as J2."""
    out = []
    for j in range(1, 7):
        name = choice.get(j) or choice.get(2)
        b = ACTUATORS.get(name, {}).get("backlash")
        out.append(ASSUMED_BACKLASH_ARCMIN if b is None else b)
    return np.array(out, dtype=float)


def tip_error(backlash, qs):
    """Per-pose, per-joint TCP displacement (mm) from the full backlash range."""
    errs = np.zeros((len(qs), 6))
    for i, q in enumerate(qs):
        J = kin.jacobian(q)
        errs[i] = np.linalg.norm(J[:3], axis=0) * backlash * ARCMIN * 1e3
    return errs


def summary(backlash, n=3000, seed=0):
    rng = np.random.default_rng(seed)
    qs = np.vstack([[0, 0, np.pi / 2, 0, 0, 0], rng.uniform(Q_MIN, Q_MAX, (n, 6))])
    e = tip_error(backlash, qs)
    return {
        "per_joint_max": e.max(axis=0),
        "per_joint_median": np.median(e, axis=0),
        "worst_sum": e.sum(axis=1).max(),            # all joints at their limit, same direction
        "worst_rss": np.sqrt((e**2).sum(axis=1)).max(),
        "median_rss": np.median(np.sqrt((e**2).sum(axis=1))),
        "stretched": e[0],
    }
