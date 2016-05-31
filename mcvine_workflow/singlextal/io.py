# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import numpy as np

def loadXtalOriConfig(path):
    from mcvine.cli import config
    xtalori = config.loadYmlConfig(path)
    l = xtalori.lattice
    for i in range(1,4):
        key = 'a%d' %i
        setattr(l, key, eval(getattr(l, key)))
        continue
    v = np.dot(l.a1, np.cross(l.a2, l.a3))
    b1 = 2*np.pi*np.cross(l.a2, l.a3)/v
    b2 = 2*np.pi*np.cross(l.a3, l.a1)/v
    b3 = 2*np.pi*np.cross(l.a1, l.a2)/v
    xo = xtalori.orientation
    for key in ['u','v']:
        setattr(xo, key, eval(getattr(xo, key)))
        continue
    from .XtalOrientation import XtalOrientation
    return XtalOrientation(b1,b2,b3, xo.u, xo.v, xo.psi)

# End of file 
