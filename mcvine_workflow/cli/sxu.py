# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
single crystal utils
"""

import os, stat, click, numpy as np

from . import workflow

@workflow.group(help="Other utils for mcvine single crystal workflow")
def sxu():
    return


@sxu.command()
@click.argument("sample")
def kernelorientation(sample):
    """Compute kernel orientation str, given sample lattice basis and uv vectors, 
This cmd needs a simplified sample yaml file. Here is an example:

\b
--- !example.yml
name: sample
lattice: 
 constants: 8.87, 8.87, 5.2, 90, 90, 90
 basis_vecotrs:
  - 8.87, 0, 0
  - 0, 8.87, 0
  - 0, 0, 5.2
orientation:
 u: 1, 0, 0
 v: 0, 1, 0

"""
    from mcvine.cli.config import loadYmlConfig
    sample = loadYmlConfig(sample)
    # parse inputs
    bv = map(eval, sample.lattice.basis_vectors)
    so=sample.orientation
    uv = map(eval, (so.u, so.v))
    from ..singlextal.scaffolding import utils
    print utils.computeOrientationStr(lattice_basis=bv, uv=uv)
    return


@sxu.command()
@click.argument("sample")
@click.argument("out")
def mkxoyml(sample, out):
    """Create xtalori.yml file
This cmd needs a simplified sample yaml file. Here is an example:

\b
--- !example.yml
name: sample
lattice: 
 constants: 8.87, 8.87, 5.2, 90, 90, 90
 basis_vecotrs:
  - 8.87, 0, 0
  - 0, 8.87, 0
  - 0, 0, 5.2
orientation:
 u: 1, 0, 0
 v: 0, 1, 0
"""
    from mcvine.cli.config import loadYmlConfig
    sample = loadYmlConfig(sample)
    # parse inputs
    bv = map(eval, sample.lattice.basis_vectors)
    from ..singlextal.scaffolding.utils import reciprocal_basis
    rb = reciprocal_basis(bv)
    b1, b2, b3 = rb
    b1 = "%s,%s,%s" % tuple(b1)
    b2 = "%s,%s,%s" % tuple(b2)
    b3 = "%s,%s,%s" % tuple(b3)
    so=sample.orientation
    u,v = so.u, so.v
    template = """
b1: %(b1)s
b2: %(b2)s
b3: %(b3)s
u: %(u)s
v: %(v)s
psi: 0
"""
    content = template % locals()
    open(out, 'wt').write(content)
    return

# End of file 
