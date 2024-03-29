# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import numpy as np
from ..sampleassembly.scaffolding.utils import reciprocal_basis


def loadXtalOriConfig(path):
    import warnings
    warnings.warn("This method is obsolete. Use loadXtalOriFromSampleYml")
    from mcvine.cli import config
    xtalori = config.loadYmlConfig(path)
    l = xtalori.lattice
    for i in range(1,4):
        key = 'a%d' %i
        setattr(l, key, eval(getattr(l, key)))
        continue
    b1,b2,b3 = reciprocal_basis([l.a1, l.a2, l.a3])
    #
    xo = xtalori.orientation
    for key in ['u','v']:
        setattr(xo, key, eval(getattr(xo, key)))
        continue
    from .XtalOrientation import XtalOrientation
    return XtalOrientation(b1,b2,b3, xo.u, xo.v, xo.psi)

def loadXtalOriFromSampleYml(path):
    from ..sample import loadSampleYml
    sample = loadSampleYml(path)
    bv = sample.lattice.basis_vectors
    b1,b2,b3 = reciprocal_basis(bv)
    xo = sample.orientation
    from .XtalOrientation import XtalOrientation
    return XtalOrientation(b1,b2,b3, xo.u, xo.v, 0)

# End of file
