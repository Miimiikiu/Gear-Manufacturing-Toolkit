"""
Copyright (c) 2023 Kieran Aponte
This software is licensed under the MIT License.
"""


from math import sin, cos, tan, pi
import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try: 
        app = adsk.core.Application.get()
        ui = app.userInterface

        #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct
        Dp, cancelled = ui.inputBox('Enter Pitch Circle Diameter', 'Diameter (mm)')
        Dp = float(Dp) * .1
        pressure_angle = 20 * pi/180
        Db = float(Dp) * cos(pressure_angle)
        if cancelled:
            exit()
        module, cancelled = ui.inputBox('Enter Module', 'Module (mm)')
        if cancelled:
            exit()
        module = float(module) * .1
        # Get the root component of the active design.
        rootComp = design.rootComponent
        comp = design.activeComponent
        Da = Dp + 2 * module
        b = 1.25 * module
        Dr = Dp - (2 * b)
        z = Dp / module

        # Create a new sketch on the xy plane.
        sketches = comp.sketches;
        xyPlane = comp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        # Get sketch health state
        health = sketch.healthState
        if health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState or health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState:        
            msg = sketch.errorOrWarningMessage

        # Get sketch points
        sketchPoints = sketch.sketchPoints
        #adsk.core.Line3D.
        circles = sketch.sketchCurves.sketchCircles
        
        pitch_circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), Dp/2)
        base_circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), Db/2)
        root_circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), Dr/2)
        addendum_circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), Da/2)
        # Create sketch point
        #point = adsk.core.Point3D.create(1.0, 1.0, 0)
        
        thetas = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
        #radius = 6 # pitch radius
        radius = Db/2 # base radius
        points = adsk.core.ObjectCollection.create()
        for theta in thetas:
            theta = theta * pi/180
            x = radius * (cos(theta) + (theta * sin(theta)))
            y = radius * (sin(theta) - (theta * cos(theta)))
            point = adsk.core.Point3D.create(x, y, 0)
            points.add(point)
        
        
            sketchPoint = sketchPoints.add(point)
        
        pitch_angle = (360 / (z*2)) * (pi/180)
        # Create mirror line    
        mirror_point = adsk.core.Point3D.create((Da/2) * cos(pitch_angle/2), (Da/2) * sin(pitch_angle/2), 0)
        mirror_line = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), mirror_point)
        #mirror_line_slope = ((Da/2) * sin(pitch_angle/2)) / ((Da/2) * cos(pitch_angle/2))
        #mirrored_slope = -1 * mirror_line_slope
        #mirror_line_slope = mirrored_slope * ()
        '''
        y = m0 * x
        y=m1 * (x-x0) + y1
        m0 * x = m1 * (x-x0) + y1
        x = m1*(x-x0)/m0 + y1/m0
        x = m1/m0 * x - m1/m0 * x0 + y1/m0
        x * (1-m1/m0) = -x0*m1/m0 + y0/m0
        x = -
        '''
        # Move sketch point
        #translation = adsk.core.Vector3D.create(1.0, 0, 0)
        #sketchPoint.move(translation)
        tooth_edge1 = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(Da/2, 0, 0))
        tooth_edge2_point = adsk.core.Point3D.create((Da/2) * cos(pitch_angle), (Da/2) * sin(pitch_angle), 0)
        tooth_edge2 = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), tooth_edge2_point)
        spline = sketch.sketchCurves.sketchFittedSplines.add(points)
        #constraints = sketch.geometricConstraints
        #symmetryConstraint = constraints.addSymmetry(test_line1, test_line2, mirror_line)



    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))