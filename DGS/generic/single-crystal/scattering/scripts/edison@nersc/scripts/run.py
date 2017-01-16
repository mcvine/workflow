#!/usr/bin/env python

import sys
id = int(sys.argv[1])

# id is SLURM_ARRAY_TASK_ID

start = -5.0
step = 0.5

angle = start + id * step

from run_oneangle import run
run(angle)

