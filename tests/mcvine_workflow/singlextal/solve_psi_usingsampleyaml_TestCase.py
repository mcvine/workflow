#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow import singlextal
from mcvine.workflow.singlextal import solve_psi

import numpy as np, os
thisdir = os.path.dirname(__file__)

Ei = 100
Etarget = 35
sample_yml_path = os.path.join(thisdir, "..", "..", 'DGS', 'ARCS', 'Si.yml')
xtalori = singlextal.loadXtalOriFromSampleYml(sample_yml_path)
hkl = [-6,0,0]
psi_min, psi_max = -5., 90.

def test_solve1():
    solutions = solve_psi.solve(xtalori, Ei, hkl, Etarget, psi_min, psi_max)
    assert len(solutions)==1
    sol = solutions[0]
    from mcvine.workflow.singlextal.misc import Eresidual
    psi, residual = Eresidual(xtalori, hkl, Etarget, [sol], Ei)[0]
    assert abs(residual) < 1e-7
    return


def main():
    test_solve1()
    print("Succeed")
    return


if __name__ == '__main__': main()

# End of file
