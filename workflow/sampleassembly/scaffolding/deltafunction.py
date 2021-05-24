# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating delta function sample
"""

import os, numpy as np

def createKernel(excitation, h2Q, orientation, srcdir, outdir):
    """
    excitation:
    - hkl
    - E
    - dE
    """
    d = dict(excitation.__dict__)
    Q = np.dot(h2Q, eval(excitation.hkl))
    Q = "%s,%s,%s" % tuple(Q)
    d.update(Q=Q, orientation=orientation)
    return kernel_template % d


kernel_template = """
    <!-- delta function kernel for resolution calculation
      Q: Q vector
      E: energy transfer (unit: meV)
      dE: allowed deviation of energy transfer (unit: meV)
      orientation: flattened rotation matrix M. M dot Q_crystal = Q_instrument
     -->
    <ConstantvQEKernel
        momentum-transfer="%(Q)s"
        energy-transfer="%(E)s*meV"
        dE="%(dE)s*meV"
        orientation="%(orientation)s"
        />
"""

# End of file 
