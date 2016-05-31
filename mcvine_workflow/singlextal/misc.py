# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import numpy as np

def Eresidual(xtalori, hkl, Etarget, angles, Ei):
    """compute residual of energy transfer
    This method compute a series of psi angle and corresponding residual 
    (E - Etarget).
    We only need to simulate crystal orientation where the residual 
    is close to zero.
    """

    from mcni.utils import conversion as conv
    ki = conv.e2k(Ei)
    kiv = np.array([ki,0,0])
    
    r = np.zeros((len(angles), 2))
    for i, psi in enumerate(angles):
        xtalori.psi = psi / 180. * np.pi
        hkl2cartesian = xtalori.hkl2cartesian_mat()
        # cart2hkl = xtalori.cartesian2hkl_mat()
        Qcart = np.dot(hkl, hkl2cartesian)
        # print hkl, np.dot(Qcart, cart2hkl)
        # print Qcart
        kfv = kiv - Qcart
        kf = np.linalg.norm(kfv)
        Ef = conv.k2e(kf)
        E = Ei - Ef
        r[i] = psi, E-Etarget
        continue
    return r

# End of file 
