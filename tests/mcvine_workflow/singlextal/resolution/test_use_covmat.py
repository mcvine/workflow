#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal.resolution import use_covmat

import numpy as np

def test():
    from mcvine_workflow.DGS import ARCS
    sampleyml = "Si.yml"
    Ei = 100
    class dynamics:
        hkl0 = [-16/3.,-8/3.,8/3.]
        hkl_dir = np.array([-1.,1.,-1.])/3
        E = 40.
        dq = 0
    class scan:
        psimin, psimax, dpsi = -5, 90., 0.5
    use_covmat.compute(ARCS, sampleyml, Ei, dynamics, scan, plot=True)
    return


def main():
    test()
    return


if __name__ == '__main__': main()

# End of file 
