#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow import singlextal
from mcvine_workflow.singlextal import coords_transform as ct
from mcvine_workflow.singlextal import solve_psi

import numpy as np

Ei = 100
Etarget = 35
xtalori = singlextal.loadXtalOriConfig("Si-xtalori.yaml")
hkl = [-6,0,0]
psi_min, psi_max = -5., 90.
# set crystal orientation to perfectly measure the given hkl
solutions = solve_psi.solve(xtalori, Ei, hkl, Etarget, psi_min, psi_max)
assert len(solutions)==1
sol = solutions[0]
xtalori.psi = sol

def test_hkl2Q():
    hkls = [hkl]
    Qs = ct.hkl2Q(hkls, xtalori)
    # print Qs
    hkls2 = ct.Q2hkl(Qs, xtalori)
    np.allclose(hkls, hkls2)
    return

def test_hklE2rtz():
    hkls = [hkl]
    r,theta,z = ct.hklE2rtz(hkls, Etarget, xtalori, Ei, r=3)
    # print r, theta, z
    E = np.array([Etarget])
    hkls2 = ct.rtzE2hkl(r, theta, z, E, xtalori, Ei)
    np.allclose(hkls, hkls2)
    return

def main():
    test_hkl2Q()
    test_hklE2rtz()
    return

if __name__ == '__main__': main()

# End of file 
