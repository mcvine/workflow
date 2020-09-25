# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating powder analytical dispersion kernel
"""

import os, numpy as np
from mcni.units import parser
parser = parser()

def createKernel(excitation):
    """
    excitation:
    - E_Q: E(Q) function
    - S_Q: S(Q) function
    - Qrange: Qmin, Qmax
    """
    d = dict(excitation.__dict__)
    Qmin, Qmax = list(map(parser.parse, d['Qrange'].split(',')))
    try:
        Qmin + Qmax + parser.parse('1./angstrom')
    except:
        raise ValueError("The units for Qrange values should be 1./angstrom. Got %s, %s" % (Qmin, Qmax))
    d['Qmin'] = Qmin; d['Qmax'] = Qmax
    check_expression(d['E_Q'])
    check_expression(d['S_Q'])
    return kernel_template % d


kernel_template = """
    <E_Q_Kernel 
       E_Q="%(E_Q)s" 
       S_Q="%(S_Q)s" 
       Qmin="%(Qmin)s"
       Qmax="%(Qmax)s"
       />
"""

def check_expression(e):
    import mccomponents.mccomponentsbp as b
    try:
        b.create_E_Q_Kernel(e, "1", 0, 10, 1., 1.)
    except Exception as exc:
        raise RuntimeError("Invalid expression %r\n%s" % (e, exc))
        

# End of file 
