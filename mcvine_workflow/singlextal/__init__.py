# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for single xtal sim workflows.

IO
* Load user-defined crystal orientation

Coordinate transformation
* Convert Q in instrument coordinate system to hkl and vice versa
* Convert r,theta,z,E (cylindrical coordinate system) to hkl,E and vice versa

Misc
* Energy transfer residual for a specific hkl,E point at a series of psi angles
* Draw scan lines
"""

from .io import loadXtalOriConfig

# End of file 
