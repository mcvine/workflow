#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow import singlextal
from mcvine_workflow.singlextal import solve_psi

import numpy as np

def test_solve():
    Ei = 100
    Etarget = 35
    xtalori = singlextal.loadXtalOriConfig("Si-xtalori.yaml")
    hkl = [-6,0,0]
    psi_min, psi_max = -5., 90.
    solutions = solve_psi.solve(xtalori, Ei, hkl, Etarget, psi_min, psi_max)
    assert len(solutions)==1
    sol = solutions[0]
    from mcvine_workflow.singlextal.misc import Eresidual
    psi, residual = Eresidual(xtalori, hkl, Etarget, [sol], Ei)[0]
    assert abs(residual) < 1e-7
    return


def main():
    test_solve()
    return


if __name__ == '__main__': main()

# End of file