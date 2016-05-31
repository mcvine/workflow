# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#
# copied from yxqd/nslice

"""data object for crystal orientation
"""

import numpy as np

class XtalOrientation:
    
    def __init__(self, b1, b2, b3, u, v, psi):
        self.b1 = np.array(b1)
        self.b2 = np.array(b2)
        self.b3 = np.array(b3)
        self.u = np.array(u)
        self.v = np.array(v)
        self.psi = psi
        return
    
    # the cartesian coordinate system uses the convention
    #  z is vertical, x along beam.
    def cartesian2hkl_mat(self):
        """output: matrix M that satisfy hkl = Q dot M, 
        where hkl and Q are all row vectors
        """
        from .xtalori import xtalori2mat
        return xtalori2mat(
            self.b1, self.b2, self.b3, 
            self.u, self.v, self.psi,
            )
    
    def hkl2cartesian_mat(self):
        """output: matrix M that satisfy Q = hkl dot M,
        where hkl and Q are row vectors
        """
        m = self.cartesian2hkl_mat()
        return np.linalg.inv(m)
    
    pass

# End of file 
