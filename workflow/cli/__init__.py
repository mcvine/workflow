# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

from mcvine.cli import mcvine

# a registry of instrumnet: beam2sample distance. used to generate sim templates
from mcvine.instruments.SEQUOIA import L_BeamEnd2Sample as SEQUOIA_L_BeamEnd2Sample
beam2sample_dict = dict(
    arcs = '0.15',
    sequoia = str(SEQUOIA_L_BeamEnd2Sample),
    cncs = '0.15',
    hyspec = '0.15',
    )

@mcvine.group()
def workflow():
    return

from . import powder, singlecrystal, sx

# obsolete cmds
from . import sxu, sxr

# End of file 
