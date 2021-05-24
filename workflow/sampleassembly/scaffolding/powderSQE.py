# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating powder S(Q,E) kernel
"""

import os, numpy as np
from mcni.units import parser
parser = parser()

def createKernel(excitation, srcdir, outdir):
    """
    excitation:
    - SQEhist: path to S(Q,E) histogram
    - Qrange: Qmin, Qmax
    - Erange: Emin, Emax
    """
    d = dict(excitation.__dict__)
    assert os.path.exists(d['SQEhist'])
    Qmin, Qmax = list(map(parser.parse, d['Qrange'].split(',')))
    try:
        Qmin + Qmax + parser.parse('1./angstrom')
    except:
        raise ValueError("The units for Qrange values should be 1./angstrom. Got %s, %s" % (Qmin, Qmax))
    Emin, Emax = list(map(parser.parse, d['Erange'].split(',')))
    try:
        Emin + Emax + parser.parse('meV')
    except:
        raise ValueError("The units for Erange values should be meV. Got %s, %s" % (Emin, Emax))
    return kernel_template % d


kernel_template = """
    <SQEkernel Q-range='%(Qrange)s' energy-range='%(Erange)s'>
      <GridSQE histogram-hdf-path="%(SQEhist)s" auto-normalization="0" />
    </SQEkernel>
"""

# End of file 
