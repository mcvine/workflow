# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
single crystal reduction
"""

import mantid, os, stat, click, numpy as np

from . import workflow

@workflow.command()
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

# End of file 
