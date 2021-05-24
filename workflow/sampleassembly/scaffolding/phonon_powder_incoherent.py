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
from ._kernel_helpers import copyfile

ext2key = {
    '.h5': 'histogram-path',
    '.idf': 'idf-data-path',
    '.txt': 'ascii-path',
    }

def createKernel(excitation, srcdir, outdir):
    """
    excitation:
    - DOS: path to DOS data
    """
    d = dict(excitation.__dict__)
    fn = d['DOS']
    basename = copyfile(fn, srcdir, outdir)
    fn, ext = os.path.splitext(fn)
    assert ext in ext2key, "Incoherent powder phonon kernel: Unknown file extension for DOS: %s" % ext
    d['dospathkey'] = ext2key[ext]
    d['DOS'] = basename
    return kernel_template % d


kernel_template = """
    <Phonon_IncoherentInelastic_Kernel>
      <LinearlyInterpolatedDOS %(dospathkey)s="%(DOS)s" />
    </Phonon_IncoherentInelastic_Kernel>
"""

# End of file
