#!/usr/bin/env python

import numpy as np, os

def main():
  for sample in np.arange(-5,90.1,0.5):
    work = 'work_%s' % sample
    if not os.path.exists(os.path.join(work, 'arcs-sim-wEidata.nxs')):
      print("missing %s" % sample)
      continue
  return

if __name__ == '__main__' : main()

