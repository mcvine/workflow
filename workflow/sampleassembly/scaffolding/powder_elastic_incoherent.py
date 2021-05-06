# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating powder incoherent elastic kernel
"""

import os, numpy as np
from mcni.units import parser
parser = parser()

def createKernel(excitation):
    """
    excitation:
    - DOS: path to DOS data
    """
    d = dict(excitation.__dict__)
    print(d)
    return kernel_template.format(**d)

kernel_template = """
    <Phonon_IncoherentElastic_Kernel
        dw_core="{dw_core}"
        scattering_xs="{scattering_xs}"
        absorption_xs="{absorption_xs}"
    />
"""

# End of file
