# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

def scattering_angle_constraints(theta, phi):
    return ((theta<135.) * (theta > 3.) + (theta < -3)*(theta>-28)) * (phi<26.565) * (phi>-26.565)


# End of file 
