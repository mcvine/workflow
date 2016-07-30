# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating spinwave sample
"""

import os, numpy as np
from .utils import computeOrientationStr, reciprocal_basis, writeXYZ, decode_chemicalformula

def createKernel(excitation, hkl, orientation):
    """
    excitation:
    - E_Q: E(vector Q) expression
    - S_Q: S(vector Q) expression
    - Emax: max energy
    """
    # hkl
    h_expr, k_expr, l_expr = hkl
    # disp
    E_Q = excitation.E_Q
    S_Q = excitation.S_Q
    Emax = excitation.Emax
    return kernel_template % locals()


kernel_template = """
    <!-- kernel for spin wave
      E_Q: expression for E(Q)
      S_Q: expression for E(Q)
      Emax: set this to maximum energy of the spin-wave excitation to help speed up the sim.
      orientation: flattened rotation matrix M. M dot Q_crystal = Q_instrument
     -->
    <E_vQ_Kernel 
	E_Q="pi:=3.1415926535897932; twopi:=2*pi; 
             h:=%(h_expr)s;
             k:=%(k_expr)s;
             l:=%(l_expr)s;
             %(E_Q)s"
	S_Q="pi:=3.1415926535897932; twopi:=2*pi; 
             h:=%(h_expr)s; 
             k:=%(k_expr)s; 
             l:=%(l_expr)s;
             %(S_Q)s"
	Emax="%(Emax)s*meV"
        orientation="%(orientation)s"
	/>
"""

# End of file 
