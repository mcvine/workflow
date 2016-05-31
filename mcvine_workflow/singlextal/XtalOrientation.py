# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#
# copied from yxqd/nslice

"""data object for crystal orientation
"""

class XtalOrientation:
    
    def __init__(self, ra, rb, rc, u, v, psi):
        self.ra = np.array(ra)
        self.rb = np.array(rb)
        self.rc = np.array(rc)
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
            self.ra, self.rb, self.rc, 
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
