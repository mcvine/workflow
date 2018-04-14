#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.sampleassembly.scaffolding import sample

import numpy as np, os
here = os.path.dirname(__file__)


def test():
    class excitation:
        type = "phonon_powder_incoherent" # match module name
        DOS = "V-dos.idf"
    sample.createSample(
        outdir='_tmp.phonon_powder_incoherent', name='sample.phonon_powder_incoherent', 
        lattice_basis = [[1,0,0],[0,1,0],[0,0,1]],
        uv = None,
        chemical_formula="Al",
        excitations = [excitation],
        add_elastic_line = False,
    )
    o = os.system('diff -r _tmp.phonon_powder_incoherent ' + os.path.join(here, 'expected-scatterer-phonon_powder_incoherent_kernel'))
    assert not o
    return


def main():
    test()
    return


if __name__ == '__main__': main()

# End of file 
