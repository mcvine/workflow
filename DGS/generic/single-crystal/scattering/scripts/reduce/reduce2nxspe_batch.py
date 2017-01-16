#!/usr/bin/env python

# reduce event nexus file into nxspe
# example of individual cmd to run
#
# $ mcvine-sns-reduce-by-mantid -nxs=arcs-sim-wEidata.nxs --psi=<psi> --powder=off --speout=sim_<psi>.nxspe

import os, subprocess as sp, numpy as np

def run(sample):
  work = 'work_%s' % sample
  infile = '%s/arcs-sim-wEidata.nxs' % work
  outfile = "nxspe-0.25meV/sim_%s.nxspe" % sample
  outfile = os.path.abspath(outfile)
  cmd = "mcvine-sns-reduce-by-mantid -nxs=%(infile)s --eaxis=-10,90,0.25 --psi=%(sample)s --powder=off --speout=%(outfile)s" % locals()
  # args = cmd.split()
  print work, cmd
  if os.system(cmd):
      print "** %s failed" % cmd
  return


def main():
  for sample in np.arange(-5,90.1,0.5):
  # for sample in np.arange(3.5,90.1,0.5):
    run(sample)
  return

if __name__ == '__main__' : main()

