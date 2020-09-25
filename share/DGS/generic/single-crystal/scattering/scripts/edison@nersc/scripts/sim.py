#!/usr/bin/env python

import os, subprocess as sp, numpy as np

def run(sample):
  print(sample)
  work = 'work_%s' % sample
  cmd = 'cp -a template %s' % work
  if not os.path.exists(work) :
    if os.system(cmd): print("%s Failed" % cmd)

  cmd = ['make', "arcs-sim-wEiData.nxs", 'SAMPLE_ANGLE=%s' % sample]
  print(' '.join(cmd))
  p = sp.Popen(cmd, stdout=sp.PIPE, cwd=work)
  out,err = p.communicate()
  return 


def main():
  for sample in np.arange(-5,90.1,0.5):
    run(sample)
  return

if __name__ == '__main__' : main()

