"""Fusion 360 script: parametric side-view skeleton of Synaptic6 (zero pose).

Run it from Utilities > Scripts and Add-Ins > Scripts > "+" (add this file) > Run.

It creates the user parameters d1, a2, d4, d6 (same names and values as
analysis/params.py) and a sketch where every link length is driven by one of
those parameters. Change a parameter and the skeleton follows.

Axis mapping: Fusion's default is Y-up, so the sketch lives on the XY plane
and the arm's "up" (z in the analysis code) is Fusion's Y.

NOT TESTED INSIDE FUSION YET. I wrote it from the API docs; if it errors,
the message box shows the traceback.
"""
import traceback
import adsk.core
import adsk.fusion

PARAMS_MM = {"d1": 120, "a2": 200, "d4": 180, "d6": 100}


def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        # user parameters only exist in a parametric design (history captured)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent

        # --- user parameters ------------------------------------------------
        for name, mm in PARAMS_MM.items():
            if design.userParameters.itemByName(name) is None:
                design.userParameters.add(
                    name, adsk.core.ValueInput.createByString(f"{mm} mm"), "mm",
                    "Synaptic6 skeleton")

        # --- sketch ---------------------------------------------------------
        sketch = root.sketches.add(root.xYConstructionPlane)
        sketch.name = "Synaptic6 skeleton (zero pose)"
        p = lambda x, y: adsk.core.Point3D.create(x, y, 0)   # cm
        d1, a2, d4, d6 = (PARAMS_MM[k] / 10 for k in ("d1", "a2", "d4", "d6"))

        lines = sketch.sketchCurves.sketchLines
        base_to_shoulder = lines.addByTwoPoints(sketch.originPoint, p(0, d1))
        upper_arm = lines.addByTwoPoints(base_to_shoulder.endSketchPoint, p(a2, d1))
        forearm = lines.addByTwoPoints(upper_arm.endSketchPoint, p(a2, d1 + d4))
        tool = lines.addByTwoPoints(forearm.endSketchPoint, p(a2, d1 + d4 + d6))
        for ln in (base_to_shoulder, upper_arm, forearm, tool):
            ln.isConstruction = True

        cons = sketch.geometricConstraints
        cons.addVertical(base_to_shoulder)
        cons.addHorizontal(upper_arm)
        cons.addVertical(forearm)
        cons.addVertical(tool)

        # --- dimensions driven by the parameters ---------------------------
        dims = sketch.sketchDimensions
        V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
        H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
        for ln, orient, name, off in (
                (base_to_shoulder, V, "d1", p(-3, d1 / 2)),
                (upper_arm, H, "a2", p(a2 / 2, d1 - 3)),
                (forearm, V, "d4", p(a2 + 3, d1 + d4 / 2)),
                (tool, V, "d6", p(a2 + 3, d1 + d4 + d6 / 2))):
            d = dims.addDistanceDimension(ln.startSketchPoint, ln.endSketchPoint,
                                          orient, off)
            d.parameter.expression = name

        # --- joint markers (J2 shoulder, J3 elbow, J5/J6 wrist centre, TCP) --
        for pt in (base_to_shoulder.endSketchPoint, upper_arm.endSketchPoint,
                   forearm.endSketchPoint, tool.endSketchPoint):
            sketch.sketchCurves.sketchCircles.addByCenterRadius(pt, 0.6)

        ui.messageBox("Skeleton created. Edit d1, a2, d4, d6 in Modify > Change Parameters.")
    except Exception:
        ui.messageBox("Failed:\n" + traceback.format_exc())
