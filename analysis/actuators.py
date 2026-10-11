"""Candidate actuators.

rated = continuous torque, peak = short bursts (Nm), mass in kg,
backlash in arcmin (None = I don't have a figure).
`checked`: True means the numbers were cross-checked on vendor/retailer pages,
False means from memory. Verify everything against the current CubeMars
datasheet before ordering.
"""
ACTUATORS = {
    # low-backlash family, figures from CubeMars/retailer pages
    "CubeMars AKE80-8":  {"rated": 12.0, "peak": 30.0, "mass": 0.57, "backlash": 9, "checked": True},
    "CubeMars AKE60-8":  {"rated": 5.0,  "peak": 12.5, "mass": 0.26, "backlash": 9, "checked": True},
    # older AK series, from memory, backlash not looked up for these ratios
    "CubeMars AK60-6":   {"rated": 3.0,  "peak": 9.0,  "mass": 0.29, "backlash": None, "checked": False},
    "CubeMars AK70-10":  {"rated": 8.3,  "peak": 24.8, "mass": 0.52, "backlash": None, "checked": False},
    "CubeMars AK80-9":   {"rated": 9.0,  "peak": 18.0, "mass": 0.49, "backlash": None, "checked": False},
    "CubeMars AK10-9":   {"rated": 18.0, "peak": 53.0, "mass": 0.96, "backlash": None, "checked": False},
    # Dynamixel: stall torque at 12 V used as "peak"; continuous is much lower
    "Dynamixel XM430-W350": {"rated": 1.4, "peak": 4.1, "mass": 0.082, "backlash": None, "checked": False},
    "Dynamixel XL430-W250": {"rated": 0.5, "peak": 1.5, "mass": 0.057, "backlash": None, "checked": False},
}

# Used by the error budget when a chosen actuator has no backlash figure.
# 15 arcmin (0.25 deg) is a guess for small servo gearboxes, not a datasheet value.
ASSUMED_BACKLASH_ARCMIN = 15
