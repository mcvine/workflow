# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating powder incoherent phonon kernel
"""

import os, numpy as np
from mcni.units import parser
parser = parser()
from ._kernel_helpers import copydirectory

def createKernel(excitation, srcdir, outdir):
    """
    excitation:
    - IDF-data-dir: path to the directory with phonon data files in IDF format
    - Ei: incident energy. E.g. "100*meV"
    - max_E: max phonon energy. E.g. "50*meV"
    - max_Q: max momentum transfer. E.g. "10./angstrom"
    """
    d = dict(excitation.__dict__)
    print(d)
    dir = d['IDF-data-dir']
    d['IDF-data-dir'] = copydirectory(dir, srcdir, outdir)
    return kernel_template.format(**d)


kernel_template = """
    <Phonon_CoherentInelastic_PolyXtal_Kernel
         Ei='{Ei}' max-omega='{max_E}' max-Q='{max_Q}'
         nMCsteps_to_calc_RARV='10000' >
      <LinearlyInterpolatedDispersion idf-data-path="{IDF-data-dir}"/>
    </Phonon_CoherentInelastic_PolyXtal_Kernel>
"""

# End of file
