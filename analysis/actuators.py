"""Candidate actuators (ready-to-use modules with integrated driver unless noted).

rated = continuous torque, peak = short bursts (Nm), mass in kg,
backlash in arcmin (None = no figure found), driver = driver board inside,
encoders = what the listings say.

Sources: CubeMars catalogue screenshots (size, weight, peak torque) plus
retailer listings for the rest. Backlash and rated torque often come from a
single retailer page, so treat every row as "to be confirmed on the datasheet".
"""
ACTUATORS = {
    # --- hollow-shaft planetary, dual 21-bit encoders, integrated driver ----
    "CubeMars AKH70-16": {"rated": 26.0, "peak": 78.0, "mass": 0.879, "backlash": 12,
                          "driver": True, "encoders": "2x 21-bit (motor + output)", "bore_mm": 7},
    "CubeMars AKH70-48": {"rated": 74.0, "peak": 222.0, "mass": 1.396, "backlash": None,
                          "driver": True, "encoders": "?", "bore_mm": 7},
    # --- AK V3 small, dual encoders, integrated driver ------------------------
    "CubeMars AK45-36 V3": {"rated": 8.0, "peak": 24.0, "mass": 0.349, "backlash": 12,
                            "driver": True, "encoders": "2x 16-bit (motor + output)", "bore_mm": 0},
    "CubeMars AK80-8 KV60": {"rated": 10.0, "peak": 25.0, "mass": 0.57, "backlash": 22.8,
                             "driver": True, "encoders": "14-bit + 15-bit", "bore_mm": 0},
    # --- AKA series, single encoder ------------------------------------------
    "CubeMars AKA60-6": {"rated": 3.0, "peak": 9.0, "mass": 0.46, "backlash": 12,
                         "driver": True, "encoders": "1 (single)", "bore_mm": 0},
    "CubeMars AKA10-9": {"rated": 18.0, "peak": 53.0, "mass": 1.06, "backlash": None,
                         "driver": True, "encoders": "1 (single)", "bore_mm": 0},
    # --- AKE: lowest backlash but sold WITHOUT driver, so not auto-selected ----
    "CubeMars AKE80-8": {"rated": 12.0, "peak": 30.0, "mass": 0.57, "backlash": 9,
                         "driver": False, "encoders": "motor side only (via driver)", "bore_mm": 0},
    "CubeMars AKE60-8": {"rated": 5.0, "peak": 12.5, "mass": 0.26, "backlash": 9,
                         "driver": False, "encoders": "?", "bore_mm": 0},
}

# Used by the error budget when a chosen actuator has no backlash figure.
ASSUMED_BACKLASH_ARCMIN = 15
