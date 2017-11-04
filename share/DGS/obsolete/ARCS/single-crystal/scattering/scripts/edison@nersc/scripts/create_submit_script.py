#!/usr/bin/env python

import numpy as np

# angles = np.arange(-3, 20, 0.5)
angles = np.arange(-5, -3, 0.5)
# angles = np.arange(-5, 90.1, 0.5)
nodes = angles.size
queue = 'regular'
cpupernode = 24
timelimit = "04:59:00"
target = "scattering"
# target = ""

cmds = ["./scripts/run_oneangle.py %s %s " % (angle, target) for angle in angles]
cmds = '\n'.join(cmds)

template = """#!/bin/bash -l
#SBATCH -p %(queue)s
#SBATCH -N %(nodes)s
#SBATCH --tasks-per-node=%(cpupernode)s
#SBATCH -t %(timelimit)s

. $HOME/.use-mcvine-at-scratch

%(cmds)s

"""

content = template % locals()

print content
