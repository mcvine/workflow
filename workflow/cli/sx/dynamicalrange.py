# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
single crystal utils for dynamical range calculation
"""

import os, stat, click, numpy as np

from . import sx

@sx.group(help="single crystal utils for dynamical range calculation")
def dynamicalrange():
    return


@dynamicalrange.command()
@click.argument("sample")
@click.option("--Ei", default=100.)
@click.option("--psi-axis", default=(-90.,90.,1.))
@click.option("--hkl0", default=(0.,0.,0.))
@click.option("--hkl-dir", default=(1.,0.,0.))
@click.option("--x-axis", default=(-5.,5.,0.1))
@click.option("--instrument", default='ARCS')
@click.option("--Erange", default=(-5.,90.))
@click.option("--out")
def slice(
        sample, 
        ei, psi_axis,
        hkl0, hkl_dir, x_axis, 
        instrument, erange,
        out):
    """dynamic range of slice"""
    from mcvine_workflow.sample import loadSampleYml
    sample = loadSampleYml(sample)
    code = "from mcvine_workflow.DGS import %s as mod" % instrument
    d = {}; exec(code, d); mod = d['mod']
    psi_angles = np.arange(*tuple(psi_axis))
    x_axis = np.arange(*tuple(x_axis))
    from matplotlib import pyplot as plt
    plt.figure()
    from ...singlextal import dynrange
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
