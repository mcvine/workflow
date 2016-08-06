# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating spinwave sample
"""

import os, numpy as np
from .utils import computeOrientationStr, reciprocal_basis, writeXYZ, decode_chemicalformula

def createKernel(excitation, h2Q, orientation):
    """
    excitation:
    - idf_dir: path to phonon data in IDF format
    """
    d = dict(excitation.__dict__)
    d.update(orientation=orientation)
    return kernel_template % d


kernel_template = """
    <Phonon_CoherentInelastic_SingleXtal_Kernel
      weight="1."
      orientation="%(orientation)s"
      >
      <LinearlyInterpolatedDispersion idf-data-path="%(idf_dir)s"/>
    </Phonon_CoherentInelastic_SingleXtal_Kernel>

    <!-- multiphonon kernel. uncomment and customize to enable -->
    <!--
    <MultiPhonon_Kernel
      Qmax="14/angstrom"
      dQ="0.05/angstrom"
      Emax="80*meV"
      weight="1."
      >
      <LinearlyInterpolatedDOS idf-path="%(idf_dir)s/DOS"/>
    </MultiPhonon_Kernel>
    -->
"""

# End of file 
