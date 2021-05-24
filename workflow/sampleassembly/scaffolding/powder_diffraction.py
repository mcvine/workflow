# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating powder diffraction kernel
"""

import os, numpy as np
from mcni.units import parser
parser = parser()
from ._kernel_helpers import copyfile

def createKernel(excitation, srcdir, outdir):
    """
    excitation:
    - Dd_over_d: path to DOS data
    - laz_path: path to laz file
    - peaks_py_path: path to peaks.py
    """
    d = dict(excitation.__dict__)
    laz = d.get('laz_path')
    if laz:
        d['laz_path'] = copyfile(laz, srcdir, outdir)
        return kernel_template_laz.format(**d)
    d['peaks_py_path'] = copyfile(d['peaks_py_path'], srcdir, outdir)
    return kernel_template_peaks_py.format(**d)

kernel_template_laz = """
    <SimplePowderDiffractionKernel
        Dd_over_d="{Dd_over_d}"
        laz-path="laz_path"
        DebyeWaller_factor="0"
    />
"""

kernel_template_peaks_py = """
    <SimplePowderDiffractionKernel
        Dd_over_d="{Dd_over_d}"
        peaks-py-path="{peaks_py_path}"
        DebyeWaller_factor="0"
    />
"""

# End of file
