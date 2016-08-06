#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal.XtalOrientation import XtalOrientation
from mcvine_workflow.singlextal.scaffolding import sample

import numpy as np

def test_phonon():
    class phonon:
        type = "phonon"
        idf_dir = "/path/to/phonon-idf-dir"
    sample.createSample(
        outdir='_tmp.phonon', name='sample.phonon', 
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = ([1,0,0], [0,1,0]),
        chemical_formula="Si",
        excitations = [phonon],
    )
    return


def main():
    test_phonon()
    return


if __name__ == '__main__': main()

# End of file 
