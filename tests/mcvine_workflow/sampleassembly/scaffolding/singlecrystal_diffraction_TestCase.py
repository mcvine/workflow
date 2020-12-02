#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.singlextal.XtalOrientation import XtalOrientation
from mcvine.workflow.sampleassembly.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)

def test_singlecrystal_diffraction():
    class sx_diffr:
        type = "singlecrystal_diffraction"
        Dd_over_d="1.e-4"
        mosaic="5./60*deg"
        lau_path="Al.lau"
    sample.createSample(
        outdir='_tmp.singlecrystal_diffraction', name='sample.singlecrystal_diffraction',
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = ([1,1,0], [0,0,1]),
        chemical_formula="Si",
        excitations = [sx_diffr],
    )
    return

def main():
    test_singlecrystal_diffraction()
    return

if __name__ == '__main__': main()

# End of file
