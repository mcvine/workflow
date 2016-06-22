#!/usr/bin/env python

# reduce event nexus file into energy events in nexus file format (not nxspe)
# so that we can use Jon's script to take slices
#
# example of individual cmd to run
#
# $ python ../../reduce/reduceKeepingEvents.py arcs-sim-wEidata.nxs -5.0 100. -10,0.25,90 reduced_-5.0.nxs

import os, subprocess as sp, numpy as np

def run(sample, Eiguess, Eaxis):
  work = 'work_%s' % sample
  outname = "reduced_%s.nxs" % sample
  if os.path.exists(os.path.join(work, outname)):
    print "skipping %s" % sample
    return
  # cmd = ['python', '../../scripts/reduceKeepingEvents.py', "sequoia-sim.nxs", "100.3", "-10,80,0.25", outname]
  cmd = ['python', '../scripts/reduce/reduceKeepingEvents.py', "sim-%s.nxs"%sample, str(sample), Eiguess, Eaxis, outname]
  print work, cmd
  p = sp.Popen(cmd, stdout=sp.PIPE, cwd=work)
  out,err = p.communicate()
  if p.wait():
    print out
    print err
  return 


def main():
  import sys
  samples = eval(sys.argv[1])
  Eiguess = sys.argv[2]
  Emin,Emax,dE = eval(sys.argv[3])
  Eaxis = '%s,%s,%s' % (Emin,dE,Emax)
  for sample in np.arange(*samples):
  # for sample in np.arange(79.5,90.1,0.5):
    run(sample, Eiguess, Eaxis)
  return

if __name__ == '__main__' : main()

