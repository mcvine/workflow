#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.singlextal.XtalOrientation import XtalOrientation
from mcvine.workflow.singlextal.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)

def test_spinwave():
    class spinwave:
        type = "spinwave"
        E_Q="2.563*sqrt(1-(cos(h*pi)*cos(k*pi))**2)"
        S_Q="1"
        Emax="10"
    sample.createSample(
        outdir='_tmp.spinwave', name='sample.spinwave', 
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = ([1,0,0], [0,1,0]),
        chemical_formula="K2V3O8",
        excitations = [spinwave],
    )
    o = os.system('diff -r _tmp.spinwave ' + os.path.join(here, 'expected-scatterer-spinwave_kernel'))
    assert not o
    return


def main():
    test_spinwave()
    return


if __name__ == '__main__': main()

# End of file 
