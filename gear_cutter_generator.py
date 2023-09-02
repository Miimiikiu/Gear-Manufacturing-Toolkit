"""
Copyright (c) 2023 Kieran Aponte
This software is licensed under the MIT License.
"""


# This script generates G Code that cuts gears on a CNC router using a gear cutting adapter.
# If your router doesn't support gear cutters, please refer to the Router Adapter STL/OBJ included in this repo.
from math import floor

##### EDIT USER VALUES #####



# Assumes mm distance
# Assumes stock is running parallel to the y axis, rotating along the y axis, and the spindle is cutting from left side
# Assumes X0 is probed to the edge of the stock and Y0 is the lowest point to cut along y (before lead-ins/outs)
# Assumes Z0 is at the center of the stock

spin = 'CW' # or CCW (when viewed looking down onto XY plane)
tool_diameter = 49.32 # diameter of cutting tool
rpm = 5000
doc = .04 # depth of cut
cutting_length = 30 # length along stock that will have the deepest grooves
#TODO: Utilize climb option
climb = False # True to cut in direction of travel. False for each tooth to slam harder into the surface.
leadin_radius = 5
leadout_radius = 5
feed_rate = 5000 
gear_teeth = 24 # teeth on gear, not gear cutter
cutter_teeth = 14
module = 1
safe_x = -5 # Should be to the left of the stock
depth_total = 2.25 # addendum circle radius - root circle radius (26/2 - 21.5/2 = 2.25)

full_rotation_distance = 16 # distance on DRO for your 4th axis to make one full rotation

filename = 'Gear_Cutter_Spur_{}Zm{}.nc'.format(gear_teeth, module)
path = 'G:\\My Drive\\NC Files\\Gears\\{}'.format(filename) # output file 

############################

assert (safe_x < 0) # Safe X should not touch stock while rotating -- BACK OFF!
assert (spin in ['CW', 'CCW'])
spin_code = 'M3' if spin == 'CW' else 'M4'

tool_radius = tool_diameter/2



steps = depth_total / doc
final_stepdown = (steps - floor(steps)) * doc
steps = floor(steps) + 1 if final_stepdown > 0 else floor(steps)

feed_per_tooth = feed_rate * (1/cutter_teeth) * (1/rpm)
print('Feed Per Tooth: {}'.format(feed_per_tooth))

print('Minimum Y Boundary:{}\nMaximum Y Boundary:{}'.format(-leadin_radius - tool_radius, cutting_length + leadout_radius + tool_radius))
print('Minimum X Boundary:{}\nMaximum X Boundary:{}'.format(min(safe_x, -leadin_radius, -leadout_radius) - tool_diameter, depth_total))

with open(path, 'w') as outfile:
    #setup
    outfile.write('({})\n\n'.format(filename))
    outfile.write('(Inspect file carefully before running!)')
    outfile.write('G90\nG17\nG21\nG94\n\nG17 G90 G94\nG54\nF{}\nG28 Z0\n\n'.format(feed_rate))
    
    #Start position
    outfile.write('G0 X{} Y{} A0\n'.format(safe_x, 0 - leadin_radius))
    outfile.write('S{} {}\n'.format(rpm, spin_code))
    outfile.write('G0 Z0\n')
    for step_number in range(steps):
        if step_number + 1 == steps and final_stepdown > 0:
            cutting_depth = final_stepdown + (step_number * doc) #depth of last step + final depth
        else:
            cutting_depth = (step_number + 1) * doc
        outfile.write('\n(DEPTH: {})\n\n'.format(cutting_depth))
        
        for tooth_number in range(gear_teeth):
            
            # Lead In 
            
            outfile.write('G01 X{} Y{}\n'.format(cutting_depth - leadin_radius, -leadin_radius))
            outfile.write('G17 G03 X{} Y{} I{} J{}\n'.format(cutting_depth, 0, 0, leadin_radius)) 
            
            outfile.write('G01 Y{}\n'.format(cutting_length))
            # Lead out
            outfile.write('G17 G03 X{} Y{} I{} J{}\n'.format(cutting_depth - leadout_radius, cutting_length + leadout_radius, -leadout_radius, 0))
            
            # Safe X & rotate
            outfile.write('G01 X{}\n'.format(safe_x))
            outfile.write('G01 Y{}\n'.format(0 - leadin_radius))
            outfile.write('G01 A{}\n'.format((full_rotation_distance / gear_teeth) * (tooth_number + 1)))
        
    outfile.write('\nM5\nG28 Z0\nM30')
        
        
       