# Gear-Manufacturing-Toolkit

## Description
A set of Python/G-Code tools, Fusion 360 plugins, and meshes for manufacturing gears

### Generate_Gear

This Fusion 360 plugin prompts you for basic information about the spur gear you want to generate, then creates the gear's sketch.

#### Usage

1. Place the Generate_Gear folder into your Fusion 360 Scripts folder. Something like C:\Users\MyName\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts
2. You may need to restart Fusion 360 when using this script for the first time.
3. To use the script, you should be in Design mode. Along the top, head to UTILITIES -> ADD-INS -> Scripts and Add-Ins (or Shift + S) -> Scripts -> Generate_Gear -> Run
4. Enter the Pitch Circle Diameter when prompted. For example, a 24Z m1 gear will have a pitch circle diamter of 24mm.
5. Enter the module.
6. You'll now see a sketch that looks like 4 concentric circles, 3 lines along the addendum circle, and a curve, centered around the origin. Head back to the SOLID tab.
7. Edit the sketch that was just created. Select the MIRROR tool. For "Objects", select the curve and for "Mirror Line", select the middle of the three lines. You'll now see the outline of a single gear tooth. Finish sketch.
8. Select the 8 sketch segments that are both inside of the addendum circle and between the two curves. Press E to extrude to a height of your choice as a new body. The sketch will automatically hide.
9. Show the sketch and extruce the root circle to the same height as a new body.
10. Select the body corresponding to the single tooth. CREATE -> Pattern -> Circular Pattern. Choose the Z axis for your axis and enter the required number of teeth. If your module is 1, this should match your pitch circle diameter.
11. Select everything created here, MODIFY -> Combine then select Join for operation and optionally New Component. Hit OK.
12. Gear created successfully! Look at all that time you saved.

<video src='./Generate_Gear_Usage.mp4' width=300/>

### Router Adapter

This is a physical attachment to a standard CNC router, which can hold a gear cutting tool with an inner diameter of 22mm. 

#### Usage

0. Carefully ensure that this adapter will safely meet your requirements and your specific setup. Use at your own risk.
1. You may need to edit the mesh if it can't fit the hole or slot on your gear cutter. The specific cutter that this was tested with is m1 PA20 #4 Z21-25 HSS and can be found here: https://www.amazon.com/gp/product/B07TT62X9Y/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1
2. You might be able to get away with resin printing the adapter with a strong resin, but you really should use something harder such as steel. The shank is designed for a 1/4" (6.35mm) collet. Don't modify the shank for a smaller size, and at the very least, make the shank from steel. You can buy a solid 1/4" rod and grind it down if needed. This is a potentially dangerous operation and you have no excuse to dodge safety recommendations.
3. To assemble, slide the metal shank into the adapter body, fit the cutter into place, and lock it in place with the nut. Screw the nut in from underneath and screw the shaft in from the side.
4. Inspect the adapter carefully to ensure that it's safe, fits snugly, and is rigid. You're now ready to rumble. For gear cutting software, please refer to gear_cutter_generator.py


### gear_cutter_generator.py

This script generates G Code that cuts gears on a CNC router using a gear cutting adapter. If your router doesn't support gear cutters, please refer to the Router Adapter STL/OBJ included in this repo.

#### Usage

Assumptions:

-You're using a standard CNC router with an adapter that allows for gear cutting, such that the gear cutter face is parallel to the XY plane.

-You're using a 4th axis that rotates parallel to the Y axis and it above the router's table.

-Your stock is cylindrical and running parallel to the Y axis, clamped firmly into the 4th axis chuch with low runout.

-Your stock is on the right side of your router and there's enough room for your safe_x to be on the left side of your stock and allows enough room for your stock to safely rotate.

-Your WCS X=0 is lightly touching the left side of the stock, your WCS Y=0 is closer to Machine Y=0, and your WCS Z=0 is in the center of your stock.

-Your specified cutting length is small enough such that it does not collide with your chuck or tailstock during leadin/out moves.

-You know what you're doing.

-You understand that use of this script and its resulting files is at your own risk.

1. Edit the user values according to your requirements, then run the file to generate the G Code file.
2. When you attach your gear cutting tool, ensure that it's facing a direction that's consistent with your specified CW/CCW spin direction. The teeth should bite into the stock like an end mill, not slide along the blunt outer edge.
3. Perform a test of the G Code file in the air first to ensure that it's functioning as you'd expect.
4. Run the generated G Code file with caution.