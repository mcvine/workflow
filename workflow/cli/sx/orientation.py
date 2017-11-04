# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
single crystal utils
"""

import os, stat, click, numpy as np

from . import sx

@sx.group(help="Other utils for mcvine single crystal workflow")
def orientation():
    return


@orientation.command()
@click.argument("sample")
def kernel(sample):
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
    from ...singlextal.scaffolding import utils
    print utils.computeOrientationStr(lattice_basis=bv, uv=uv)
    return


@orientation.command()
@click.argument("sample")
@click.option("--Ei", default=100.)
@click.option("--hkl", default=(1.,0.,0.))
@click.option("--E", default=50.)
@click.option("--psimin", default=-90.)
@click.option("--psimax", default=90.)
@click.option("--number-segments", default=10)
def solve_psi(sample, ei, hkl, e, psimin, psimax, number_segments):
    "compute psi angle"
    from ...singlextal.io import loadXtalOriFromSampleYml
    xtalori = loadXtalOriFromSampleYml(sample)
    from ...singlextal.solve_psi import solve
    results = solve(
        xtalori, ei, hkl, e, psimin, psimax,
        Nsegments = number_segments)
    from ...singlextal.coords_transform import hkl2Q
    for r in results:
        xtalori.psi = r*np.pi/180.
        print "psi=%s, Q=%s" % (r, hkl2Q(hkl, xtalori))
        print "hkl2Q=%r\n(Q = hkl dot hkl2Q)" % (xtalori.hkl2cartesian_mat(),)
    return


# End of file 
