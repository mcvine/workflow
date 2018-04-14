#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.sampleassembly.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)


def test_powdersqe():
    class powdersqe:
        type = "powderSQE"
        SQEhist = "Al-iqe.h5"
        Erange = "-50*meV,50*meV"
        Qrange = "0/angstrom, 10/angstrom"
    sample.createSample(
        outdir='_tmp.powdersqe', name='sample.powdersqe', 
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = None,
        chemical_formula="Al",
        excitations = [powdersqe],
        add_elastic_line = False,
    )
    o = os.system('diff -r _tmp.powdersqe ' + os.path.join(here, 'expected-scatterer-powdersqe_kernel'))
    assert not o
    return


def main():
    test_powdersqe()
    return


if __name__ == '__main__': main()

# End of file 
