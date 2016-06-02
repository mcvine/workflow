# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import scipy.optimize

def solve(
        xtalori, Ei, hkl, E, psi_min, psi_max, 
        Nsegments = 10,
        solver=scipy.optimize.brentq):
    """search for the psi angle that allows for minimal discrepancy
    between desired energy transfer and energy transfer computed from
    scattering triangle Q = ki - kf
    
    Inputs:
    - xtalori: crystal orientation object. psi will be varied to find the optimal one
    - Ei: incident energy in meV
    - hkl: desired hkl
    - E: desired energy transfer
    - psi_min, psi_max: psi bracket (degrees)
    """
    from .misc import Eresidual
    def res(angles):
        single_value = False
        try: 
            iter(angles)
        except TypeError:
            single_value = True
            angles = [angles]            
        r = Eresidual(xtalori, hkl, E, angles, Ei)
        residuals = r[:, -1]
        if single_value:
            return residuals[0]
        return residuals
    
    delta = 1.*(psi_max-psi_min)/Nsegments
    results = []
    for i in range(Nsegments):
        min = psi_min+i*delta
        max = min + delta
        try:
            results.append(solver(res, min, max))
        except:
            pass
        continue
    return results
            

# End of file 
