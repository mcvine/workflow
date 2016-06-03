# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
hkl2Q and Q2hkl:
* hkl: miller indices
* Q: cartesian in instrument coordinate system
     in which z is vertical and x is along beam

rtzE:
* r, theta, z: cylindrical coordinate system. z vertical. x along beam
  - r,z: meters
  - theta: radian
* for DGS, Ei is needed for computing Ef

"""

import numpy as np
from mcni.utils import conversion as conv

def hkl2Q(hkl, xtalori):
    """hkl: hkl vectors (N,3)
    """
    m = xtalori.hkl2cartesian_mat()
    return np.dot(hkl, m)

def Q2hkl(Q, xtalori):
    """Q: Q vectors (N,3)
    """
    m = xtalori.cartesian2hkl_mat()
    return np.dot(Q, m)

def rtzE2hkl(r, theta, z, E, xtalori, Ei):
    """convert from cylinderical coordinate sytem to hkl
    """
    kf_dir = [r*np.cos(theta), r*np.sin(theta), z]
    kf_dir /= np.linalg.norm(kf_dir)
    Ef = Ei - E
    kf_scalar = (conv.SE2V*conv.V2K) * Ef**.5
    kf = kf_dir * kf_scalar
    ki_scalar = conv.e2k(Ei)
    ki = [ki_scalar, 0, 0]
    Q = ki - kf
    return Q2hkl(Q, xtalori)

def hklE2rtz(hkl, E, xtalori, Ei, r):
    """convert from hkl to cylinderical coordinate sytem
    """
    ki_scalar = conv.e2k(Ei)
    ki = [ki_scalar, 0, 0]
    Q = hkl2Q(hkl, xtalori)
    kf = ki - Q
    kf_dir = kf/np.linalg.norm(kf)
    scale_factor = r/np.linalg.norm(kf_dir[:, :3])
    position = kf_dir * scale_factor
    np.allclose(np.linalg.norm(position[:, :3]), r)
    theta = np.arctan2(position[:, 1], position[:, 0])
    return r, theta, position[:, 2]

# End of file 
