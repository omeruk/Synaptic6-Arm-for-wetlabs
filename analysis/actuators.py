"""Candidate actuators. Numbers are from memory of the datasheets, rounded.
VERIFY every row against the current vendor datasheet before relying on it.
rated = continuous torque, peak = short bursts (Nm), mass in kg.
"""
ACTUATORS = {
    "CubeMars AK60-6":   {"rated": 3.0,  "peak": 9.0,  "mass": 0.29},
    "CubeMars AK70-10":  {"rated": 8.3,  "peak": 24.8, "mass": 0.52},
    "CubeMars AK80-9":   {"rated": 9.0,  "peak": 18.0, "mass": 0.49},
    "CubeMars AK10-9":   {"rated": 18.0, "peak": 53.0, "mass": 0.96},
    # Dynamixel: stall torque at 12 V used as "peak"; continuous is much lower.
    "Dynamixel XM430-W350": {"rated": 1.4, "peak": 4.1, "mass": 0.082},
    "Dynamixel XL430-W250": {"rated": 0.5, "peak": 1.5, "mass": 0.057},
}
