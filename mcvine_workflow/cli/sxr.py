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
def reduce():
    return

# End of file 
