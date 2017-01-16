#!/usr/bin/env python

import numpy as np, os
from sim import run

def main():
  for sample in np.arange(-5,90.1,0.5):
    work = 'work_%s' % sample
    if os.path.exists(os.path.join(work, 'arcs-sim-wEidata.nxs')):
    # if os.path.exists(os.path.join(work, 'log.scatter')): # this is used when sometimes the job got put into hold, and it is not running by the queueing system. in that case, the jobs that are on hold need to be killed, and then we can rerun this script to resubmit the jobs
      print "skipping %s" % sample
      continue
    run(sample)
  return

if __name__ == '__main__' : main()

