# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
single crystal reduction
"""

slice_yml_example = """
Eaxis:
 min: 0
 max: 90
 N: 181
Q_projections:
 U:
  proj: 1,0,0
  proj_name: H,0,0
  min: -5
  max: 5
  N: 251
 V:
  proj: 0,1,0
  proj_name: 0,K,0
  min: -1
  max: 1
  N: 1
 W:
  proj: 0,0,1
  proj_name: 0,0,L
  min: -1
  max: 1
  N: 1
"""

import os, stat, click, numpy as np

from . import workflow

@workflow.group()
def sxr():
    return

@sxr.command()
@click.option("--instrument-type", default='DGS', type=click.Choice(['DGS']))
@click.option("--type", default="batch", type=click.Choice(['batch', 'single']))
@click.option("--eiguess", default=100.)
@click.option("--eaxis", default=(0.,100.,1.), nargs=3, type=float)
@click.option("--psi-axis", default=(-10., 120., 1.), nargs=3, type=float)
@click.option("--psi", default=0.)
@click.option("--eventnxs", help='type=single: event nxs filename, type=batch: event nxs filename template')
@click.option("--out", help='type=single: output filename, type=batch: output filename template')
def reduce(instrument_type, type, eiguess, eaxis, psi_axis, psi, eventnxs, out):
    assert instrument_type == 'DGS'
    eventnxs = eventnxs.encode()
    out = out.encode()
    from mcvine_workflow.singlextal import reduction
    if type == 'single':
        reduction.reduceOneKeepingEvents(eventnxs, psi, eiguess, eaxis, out)
    elif type == 'batch':
        reduction.reduceScan(psi_axis, eventnxs, out, eiguess, eaxis)
    return


@sxr.command()
@click.option("--sample", default='sample.yml')
@click.option("--psi-axis", default=(-10., 120., 1.), nargs=3, type=float)
@click.option("--nxs", default='reduced_%s.nxs', help='input filename pattern for reduced nxs files')
@click.option("--slice", default='slice.yml')
@click.option("--out", default='out.nxs')
def slice(sample, psi_axis, nxs, slice, out):
    from mcvine.cli.config import loadYmlConfig
    # load sample
    sample = loadYmlConfig(sample)
    lattice_params = eval(sample.lattice.constants)
    orientation = sample.orientation
    # load scan
    angles = np.arange(*psi_axis)
    nxs = nxs.encode()
    filenames = [
        nxs % dict(angle=angle)
        for angle in angles
    ]
    print angles[0], filenames[0]
    # load slice
    slice = loadYmlConfig(slice)
    Eaxis = slice.Eaxis
    Qproj_axes = slice.Q_projections
    out = out.encode()
    from mcvine_workflow.singlextal import reduction
    reduction.getslice(
        angles, filenames, lattice_params, orientation, Eaxis, Qproj_axes, out)
    return


@sxr.command(help="Convert mantid-create slice nxs file to histogram h5 file")
@click.argument("mantid")
@click.argument("histogram")
def slice2hist(mantid, histogram):
    mantid = mantid.encode()
    histogram = histogram.encode()
    from mcvine_workflow.singlextal import reduction
    reduction.slice2hist(mantid, histogram)

# End of file 
