"""
tools to compute dynamic range of a single crystal scan
"""

import numpy as np
from mcni.utils import conversion as Conv


def plotDynRangeOfSlice(
        sample, psi_angles, Ei,
        hkl0, hkl_dir, xaxis, 
        scattering_angle_constraints,
        Erange=None):
    from matplotlib import pyplot as plt
    for psi, xs, Es in iterPointsInSlice(
            sample, psi_angles, Ei,
            hkl0, hkl_dir, xaxis,
            scattering_angle_constraints,
            Erange=Erange):
        plt.plot(xs, Es, label=str(psi))
        continue
    # plt.legend()
    return


def iterPointsInSlice(
        sample, psi_angles, Ei, hkl0, hkl_dir, xaxis, 
        scattering_angle_constraints,
        Erange = None):
    """iterate over points measured in the given slice
    """
    # linear
    # xaxis = np.arange(xmin, xmax+dx/2, dx)
    # random
    # xaxis = XMIN + np.random.random(200)*(XMAX-XMIN)
    lattice_basis = sample.lattice.basis_vectors
    from ..sampleassembly.scaffolding.utils import reciprocal_basis
    b1,b2,b3 = reci_basis = reciprocal_basis(lattice_basis)
    so = sample.orientation
    u,v = so.u, so.v
    if Erange is not None:
        Emin, Emax = Erange
    from .XtalOrientation import xtalori2mat
    DEG2RAD = np.pi/180
    for psi_in_deg in psi_angles:
        psi = psi_in_deg * DEG2RAD
        M = np.array(xtalori2mat(b1,b2,b3, u, v, psi))
        # mat in compute_xE_curve requires Q = hkl dot mat, Q and hkl are row vectors
        # the M from xtalori2mat satisfies hkl = Q dot M
        # so mat = M^{-1}
        mat = np.linalg.inv(M)
        ex = np.array(hkl_dir)
        hkl0 = np.array(hkl0)
        E, theta, phi = compute_xE_curve(xaxis, hkl0, ex, mat, Ei=Ei)
        theta /= DEG2RAD
        phi /= DEG2RAD
        # pylab.plot(xaxis,E)
        limit = scattering_angle_constraints(theta, phi)
        if Erange is not None:
            limit *= E>Emin
            limit *= E<Emax
        xaxis1 = xaxis[limit]
        E1 = E[limit]
        yield psi_in_deg, xaxis1, E1
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


