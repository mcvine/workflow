#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.sampleassembly.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)


def test():
    class excitation:
        type = "powder_analytical_dispersion" # match module name
        E_Q = "sin(Q)"
        S_Q = "1."
        Qrange = "0/angstrom, 10/angstrom"
    sample.createSample(
        outdir='_tmp.powder_analytical_dispersion', name='sample.powder_analytical_dispersion', 
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = None,
        chemical_formula="Al",
        excitations = [excitation],
        add_elastic_line = False,
    )
    o = os.system('diff -r _tmp.powder_analytical_dispersion ' + os.path.join(here, 'expected-scatterer-powder_analytical_dispersion_kernel'))
    assert not o
    return


def main():
    test()
    return


if __name__ == '__main__': main()

# End of file 
