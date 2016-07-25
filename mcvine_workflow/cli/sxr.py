# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
single crystal reduction
"""

import os, stat, click

from . import workflow

@workflow.command()
@click.option("--instrument-type", default='DGS', type=click.Choice(['DGS']))
@click.option("--type", default="batch", type=click.Choice(['batch', 'single']))
@click.option("--eiguess", default=100.)
@click.option("--eaxis", default=(0.,100.,1.), nargs=3, type=float)
@click.option("--psi-axis", default=(-10., 120., 1.), nargs=3, type=float)
@click.option("--psi", default=0.)
@click.option("--eventnxs")
@click.option("--out")
def reduce(instrument_type, type, eiguess, eaxis, psi_axis, psi, eventnxs, out):
    print (instrument_type, type, eiguess, eaxis, psi_axis, psi, eventnxs, out)
    return

# End of file 
