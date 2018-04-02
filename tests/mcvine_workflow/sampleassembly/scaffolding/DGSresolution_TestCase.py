#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.sampleassembly.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)


def test_dgsresolution():
    class dgsresolution:
        type = "DGSresolution"
        target_position = "3*meter,0*meter,0*meter"
        target_radius = "0.5*inch"
        tof_at_target = "4000*microsecond"
        dtof = "10.*microsecond"
    sample.createSample(
        outdir='_tmp.dgsresolution', name='sample.DGSResolution',
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = ([1,0,0], [0,1,0]),
        chemical_formula="Si",
        excitations = [dgsresolution],
        add_elastic_line = False,
    )
    o = os.system('diff -r _tmp.dgsresolution ' + os.path.join(here, 'expected-scatterer-DGSResolution_kernel'))
    assert not o
    return


def main():
    test_dgsresolution()
    return


if __name__ == '__main__': main()

# End of file 
