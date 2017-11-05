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


# implementation details
def xtalori2mat(b1, b2, b3, u, v, psi):
    """create transformation matrices from orientation spec
    inputs: reciprocal laticce vectors, u/v vectors, and psi angle
    output: matrix M that satisfy hkl = Q dot M, where hkl and Q are all row vectors
    
    b1, b2, b3 are reciprocal base vectors represented in a cartesian
    coordinate system attached to the crystal.
    
    u/v vectors are vectors in the rotation plane of the crystal
    represented in hkl notation.
    
    The main goal here is to compute three unit vectors
    represented in hkl notation: x, y, z.
    Here z is vertical, x along beam.
    
    u/v vectors are in the x-y plane.
    if psi is 0, u should be x, and v must be in x-y plane.
    """
    # b1, b2, b3 are defined in a cartesian
    # coordinate system attached to the crystal (CCSC)
    r = np.array([b1, b2, b3], dtype=float)
    # compute u, v in cartesian coordinate system
    u_cart = np.dot(u, r)
    v_cart = np.dot(v, r)
    # normalize them
    lu = np.linalg.norm(u_cart); u_cart/=lu
    lv = np.linalg.norm(v_cart); v_cart/=lv
    # u and v is not necesarily perpendicular to each other
    # let us compute z first
    ez = np.cross(u_cart, v_cart); ez/=np.linalg.norm(ez)
    # now we can compute vprime, a unit vector perpedicular to
    # u_cart and ez
    vprime_cart = np.cross(ez, u_cart)
    # rotate u, v by psi angle to obtain x,y unit vectors
    from math import cos, sin
    ex = u_cart * cos(psi) - vprime_cart * sin(psi)
    ey = u_cart * sin(psi) + vprime_cart * cos(psi)
    # now express xyz with b1, b2, b3, to get hkl
    # dot(r.T, hkl) = cartesian, therefore, dot(r.T**-1, cartesian) = hkl
    invR = np.linalg.inv(r.T)
    x1 = np.dot(invR, ex)
    y1 = np.dot(invR, ey)
    z1 = np.dot(invR, ez)
    return np.array([x1, y1, z1])

# End of file 
