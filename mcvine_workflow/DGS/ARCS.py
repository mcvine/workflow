# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

L_PM=11.61
R = 3.
L_PS=13.6

def scattering_angle_constraints(theta, phi):
    return ((theta<135.) * (theta > 3.) + (theta < -3)*(theta>-28)) * (phi<26.565) * (phi>-26.565)


# End of file 
