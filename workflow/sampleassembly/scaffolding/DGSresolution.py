# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
DGSresolution kernel
"""

import os, numpy as np

def createKernel(excitation, h2Q, orientation, srcdir, outdir):
    """
    excitation:
    - target_position
    - target_radius
    - tof_at_target
    - dtof
    """
    d = dict(excitation.__dict__)
    # DEV NOTE: it is more tourblesome to use the orientation matrix with this kernel
    # DEV NOTE: so we don't use it here, in contrast to other kernels that use hkl
    return kernel_template % d


kernel_template = """
    <!-- DGS resolution kernel
      target-position: target position. example: 2.87121987*meter,0.*meter,8.69538059e-01*meter
      target-radius: rough estimate of target radius
      tof-at-target: TOF at target
      dtof: TOF width thru target
     -->
    <DGSSXResKernel
        target-position="%(target_position)s"
        target-radius="%(target_radius)s"
        tof-at-target="%(tof_at_target)s"
        dtof="%(dtof)s"
        />
"""

# End of file 
