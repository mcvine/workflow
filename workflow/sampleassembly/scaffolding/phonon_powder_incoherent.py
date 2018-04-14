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


ext2key = {
    '.h5': 'histogram-path',
    '.idf': 'idf-data-path',
    '.txt': 'ascii-path',
    }

def createKernel(excitation):
    """
    excitation:
    - DOS: path to DOS data
    """
    d = dict(excitation.__dict__)
    path = d['DOS']
    assert os.path.exists(path), "%s does not exist" % path
    fn, ext = os.path.splitext(path)
    assert ext in ext2key, "Incoherent powder phonon kernel: Unknown file extension for DOS: %s" % ext
    d['dospathkey'] = ext2key[ext]
    return kernel_template % d


kernel_template = """
    <Phonon_IncoherentInelastic_Kernel>
      <LinearlyInterpolatedDOS %(dospathkey)s="%(DOS)s" /> 
    </Phonon_IncoherentInelastic_Kernel>
"""

# End of file 
