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

class instrument:
    def __init__(
            self, name, detsys_radius, L_m2s, offset_sample2beam, L_m2fc=None,
            detsys_shape = 'cylinder', pixel_orientation_func = None
    ):
        """create instrument instance

        Parameters
        ----------

        name : str
            name. e.g. ARCS
        detsys_radius : str
            radius of detector system. e.g. 3*meter
        L_m2s : str
            moderator sample distance. e.g. 13.6*meter
        offset_sample2beam : str
            sample to beam-saved position. e.g. -0.15*meter
        detsys_shape : str
            shape of detector system. cylinder or sphere
        pixel_orientation_func : function
            function to calculation pixel orientation matrix
            (mcstas convention: z-beam, y-vertical)
            inputs are theta and phi of the pixel in radian
            (spherical coord system, z-vertical, x-beam)
            e.g.
            >>> rotmat = pixel_orientation_func(theta, phi)
        """
        self.name = name
        self.detsys_radius = detsys_radius
        assert detsys_shape in ['cylinder', 'sphere']
        self.detsys_shape = detsys_shape
        self.L_m2s = L_m2s
        self.offset_sample2beam = offset_sample2beam
        self.L_m2fc = L_m2fc
        self.pixel_orientation_func = pixel_orientation_func

class pixel:
    def __init__(self, radius, height, pressure, position=None, orientation=None):
        self.radius = radius
        self.height = height
        self.pressure = pressure
        self.position = position
        self.orientation = orientation

class axis:
    def __init__(self, min, max, step):
        self.min, self.max, self.step = min, max, step

    def ticks(self):
        import numpy as np
        return np.arange(self.min, self.max, self.step)

class dynamics:

    def __init__(self, E, q, hkl0, hkl_dir):
        self.E = E
        self.q = q
        self.hkl0 = hkl0
        self.hkl_dir = hkl_dir

from .io import loadXtalOriConfig, loadXtalOriFromSampleYml

# End of file
