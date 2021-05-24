#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.singlextal.XtalOrientation import XtalOrientation
from mcvine.workflow.sampleassembly.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)

def test_phonon():
    class phonon:
        type = "phonon"
        idf_dir = "phonon-idf-dir"
    outdir = '_tmp.phonon'
    if os.path.exists(outdir):
        import shutil
        shutil.rmtree(outdir)
    sample.createSample(
        outdir=outdir, name='sample.phonon',
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = ([1,0,0], [0,1,0]),
        chemical_formula="Si",
        excitations = [phonon],
    )
    o = os.system('diff -r _tmp.phonon ' + os.path.join(here, 'expected-scatterer-phonon_kernels'))
    assert not o
    return


def main():
    test_phonon()
    return


if __name__ == '__main__': main()

# End of file 
