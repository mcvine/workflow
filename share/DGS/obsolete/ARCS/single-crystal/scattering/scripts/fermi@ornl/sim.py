#!/usr/bin/env python

import os, subprocess as sp, numpy as np

def run(sample):
  print(sample)
  work = 'work_%s' % sample
  if not os.path.exists(work):
    cmd = 'cp -a template %s' % work
    if os.system(cmd): 
      print("%s Failed" % cmd)
      return
  cmd = ['make', "arcs-sim-wEiData.nxs", 'SAMPLE_ANGLE=%s' % sample]
  cmd = ' '.join(cmd)
  scriptpath = os.path.join(work, 's')
  open(scriptpath, 'at').write('\n%s\n' % cmd)
  submitcmd = 'qsub s'
  p = sp.Popen(submitcmd, shell=True, cwd=work)
  if p.wait():
    print("%s failed" % submitcmd)
  return 


def main():
  for sample in np.arange(-5,90.1,0.5):
  # for sample in np.arange(-4,90.1,0.5):
  # for sample in np.arange(-5,-4,0.5):
    print('* %s' % sample)
    run(sample)
  return

if __name__ == '__main__' : main()

