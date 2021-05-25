# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating single crystal diffraction sample
"""

import os, numpy as np
from ._kernel_helpers import copyfile

def createKernel(excitation, h2Q, orientation, srcdir, outdir):
    """
    excitation:
      Dd_over_d="1.e-4" lau_path="Al.lau" mosaic="5./60*deg"
    """
    d = dict(excitation.__dict__)
    lau = d['lau_path']
    d['lau_path'] = copyfile(lau, srcdir, outdir)
    d.update(orientation=orientation)
    return kernel_template % d


kernel_template = """
      <SingleCrystalDiffractionKernel
        weight="1."
        orientation="%(orientation)s"
        Dd_over_d="%(Dd_over_d)s"
        lau-path="%(lau_path)s"
        mosaic="%(mosaic)s"
      >
      </SingleCrystalDiffractionKernel>
"""

# End of file
