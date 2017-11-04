# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
single crystal utils
"""

import os, stat, click, numpy as np

from . import workflow

@workflow.group(help="OBSOLETE: Other utils for mcvine single crystal workflow")
def sxu():
    return


@sxu.command()
@click.argument("sample")
def kernelorientation(sample):
    """OBSOLETE: use "mcvine workflow sx orientation kernel" instead.

Compute kernel orientation str, given sample lattice basis and uv vectors, 
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
@click.option("--Ei", default=100.)
@click.option("--hkl", default=(1.,0.,0.))
@click.option("--E", default=50.)
@click.option("--psimin", default=-90.)
@click.option("--psimax", default=90.)
@click.option("--number-segments", default=10)
def solve_psi(sample, ei, hkl, e, psimin, psimax, number_segments):
    """OBSOLETE: use "mcvine workflow sx orientation solve_psi" instead"""
    from ..singlextal.io import loadXtalOriFromSampleYml
    xtalori = loadXtalOriFromSampleYml(sample)
    from ..singlextal.solve_psi import solve
    results = solve(
        xtalori, ei, hkl, e, psimin, psimax,
        Nsegments = number_segments)
    for r in results:
        print r
    return


@sxu.command()
@click.argument("sample")
@click.option("--Ei", default=100.)
@click.option("--psi-axis", default=(-90.,90.,1.))
@click.option("--hkl0", default=(0.,0.,0.))
@click.option("--hkl-dir", default=(1.,0.,0.))
@click.option("--x-axis", default=(-5.,5.,0.1))
@click.option("--instrument", default='ARCS')
@click.option("--Erange", default=(-5.,90.))
@click.option("--out")
def dr_slice(
        sample, 
        ei, psi_axis,
        hkl0, hkl_dir, x_axis, 
        instrument, erange,
        out):
    """OBSOLETE: use "mcvine workflow sx dynamicalrange slice" instead"""
    from mcvine_workflow.sample import loadSampleYml
    sample = loadSampleYml(sample)
    code = "from mcvine_workflow.DGS import %s as mod" % instrument
    d = {}; exec(code, d); mod = d['mod']
    psi_angles = np.arange(*tuple(psi_axis))
    x_axis = np.arange(*tuple(x_axis))
    from matplotlib import pyplot as plt
    plt.figure()
    from ..singlextal import dynrange
    dynrange.plotDynRangeOfSlice(
        sample, psi_angles, ei, hkl0, hkl_dir, x_axis,
        mod.scattering_angle_constraints,
        Erange=erange)
    if out:
        plt.savefig(out)
    else:
        plt.show()
    return

# End of file 
