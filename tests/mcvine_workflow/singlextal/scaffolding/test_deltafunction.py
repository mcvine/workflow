#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal.scaffolding import sample

import numpy as np

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
    return


def main():
    test_deltafunction()
    return


if __name__ == '__main__': main()

# End of file 
