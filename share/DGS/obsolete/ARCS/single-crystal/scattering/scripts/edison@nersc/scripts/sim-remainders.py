#!/usr/bin/env python

import numpy as np, os
from sim import run

def main():
  for sample in np.arange(-5,90.1,0.5):
    work = 'work_%s' % sample
    if os.path.exists(os.path.join(work, 'arcs-sim-wEidata.nxs')):
      print "skipping %s" % sample
      continue
    run(sample)
  return

if __name__ == '__main__' : main()

