# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
DGSresolution kernel
"""

import os, numpy as np

def createKernel(excitation, h2Q, orientation):
    """
    excitation:
    - target_position
    - target_radius
    - tof_at_target
    - dtof
    """
    d = dict(excitation.__dict__)
    d.update(orientation=orientation)
    return kernel_template % d


kernel_template = """
    <!-- DGS resolution kernel
      target-position: target position. example: 2.87121987*meter,0.*meter,8.69538059e-01*meter
      target-radius: rough estimate of target radius
      tof-at-target: TOF at target
      dtof: TOF width thru target
      orientation: flattened rotation matrix M. M dot Q_crystal = Q_instrument
     -->
    <ConstantvQEKernel
        target-position="%(target_position)s"
        target-radius="%(target_radius)s"
        tof-at-target="%(tof_at_target)s"
        dtof="%(dtof)s"
        orientation="%(orientation)s"
        />
"""

# End of file 
