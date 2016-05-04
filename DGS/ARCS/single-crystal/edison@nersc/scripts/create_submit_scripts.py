#!/usr/bin/env python

import numpy as np

# angles = np.arange(-3, 20, 0.5)
# angles = np.arange(-4.5, 0, 0.5)
# angles = np.arange(-5, 90.1, 0.5)
angles = np.arange(-4.5, 90.1, 0.5)
queue = 'regular'
cpupernode = 24
target = ""
title = "300K"
nodes = 8
hourspertask = .5

taskspernode = len(angles)//nodes
timelimit = "%02d:00:00" % (int(taskspernode*hourspertask+1),)

template = """#!/bin/bash -l
#SBATCH -p %(queue)s
#SBATCH --qos=premium
#SBATCH -N 1
#SBATCH --tasks-per-node=%(cpupernode)s
#SBATCH -t %(timelimit)s
#SBATCH -J %(name)s

. $HOME/.use-mcvine-at-scratch

%(cmds)s

"""
for node in range(nodes):
    angles1 = angles[node*taskspernode:(node+1)*taskspernode]
    cmds = ["./scripts/run_oneangle.py %s %s " % (angle, target) for angle in angles1]
    cmds = '\n'.join(cmds)
    name = "%s..%s-%s" % (angles1[0], angles1[-1], title)
    content = template % locals()
    script_fn = "node%s..%s.sh" % (angles1[0], angles1[-1])
    open(script_fn, 'wt').write(content)
