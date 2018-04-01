#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.singlextal.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)


def test_deltafunction():
    class deltafunction:
        type = "deltafunction"
        hkl = "0,1,0"
        E = 30
        dE = 0.05
    sample.createSample(
        outdir='_tmp.deltafunction', name='sample.deltafunction', 
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = ([1,0,0], [0,1,0]),
        chemical_formula="Si",
        excitations = [deltafunction],
        add_elastic_line = False,
    )
    o = os.system('diff -r _tmp.deltafunction ' + os.path.join(here, 'expected-scatterer-deltafunction_kernel'))
    assert not o
    return


def main():
    test_deltafunction()
    return


if __name__ == '__main__': main()

# End of file 
