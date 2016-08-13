"""
tools to compute dynamic range of a single crystal scan
"""

import numpy as np
from mcni.utils import conversion as Conv

def iterPointsInSlice(sample, psi_angles, Ei, hkl0, hkl_dir, xaxis):
    """iterate over points measured in the given slice
    """
    # linear
    # xaxis = np.arange(xmin, xmax+dx/2, dx)
    # random
    # xaxis = XMIN + np.random.random(200)*(XMAX-XMIN)
    lattice_basis = sample.lattice.basis_vectors
    from .scaffolding.utils import reciprocal_basis
    b1,b2,b3 = reci_basis = reciprocal_basis(lattice_basis)
    so = sample.orientation
    u,v = so.u, so.v
    from .XtalOrientation import xtalori2mat
    DEG2RAD = np.pi/180
    for psi in psi_angles:
        psi = psi * DEG2RAD
        M = np.array(xtalori2mat(b1,b2,b3, u, v, psi))
        # mat in compute_xE_curve requires Q = hkl dot mat, Q and hkl are row vectors
        # the M from xtalori2mat satisfies hkl = Q dot M
        # so mat = M^{-1}
        mat = np.linalg.inv(M)
        ex = np.array(hkl_dir)
        hkl0 = np.array(hkl0)
        E, theta, phi = compute_xE_curve(xaxis, hkl0, ex, mat, Ei=Ei)
        # pylab.plot(xaxis,E)
        limit = ((theta<135.*DEG2RAD) * (theta > 3.*DEG2RAD) + (theta < -3*DEG2RAD)*(theta>-28*DEG2RAD)) * (phi<26.565*DEG2RAD) * (phi>-26.565*DEG2RAD)
        xaxis1 = xaxis[limit]
        E1 = E[limit]
        yield psi, xaxis1, E1
        continue
    return


def compute_xE_curve(xaxis, hkl0, ex, mat, Ei):
    """given xaxis and ex, compute hkl = hkl0+ x*ex
    and then compute energy transfer E
    
    mat: convert hkl to Q
    """
    ki = Conv.e2k(Ei)
    kiv = np.array([ki, 0, 0])
    hkl = hkl0 + xaxis[:, np.newaxis] * ex
    Q = np.dot(hkl, mat) # NX3
    kfv = kiv - Q # NX3
    kf2 = np.sum(kfv**2, -1) # N
    kf = np.sqrt(kf2) # N

    # theta is the angle in the scattering plane (x-y)
    theta = np.arctan2(kfv[:, 1], kfv[:, 0]) # N
    # phi is the angle off the scattering plane. sin(phi) = z/r
    phi = np.arcsin(kfv[:, 2], kf)

    Ef = kf2 * (Conv.K2V**2 * Conv.VS2E)
    E = Ei - Ef
    return E, theta, phi


