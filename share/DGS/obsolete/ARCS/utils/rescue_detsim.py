#!/usr/bin/env python

"""rescue the detector simulation

Sometimes the detector simulation will fail to merge
the events.dat file.
As a result, the arcs-sim*.nxs files are not generated.

This script first merge the events.dat,
and then call make to generate nxs files.
"""


import sys, os

def run(workdir):
    res = os.path.join(workdir, 'arcs-sim-wEidata.nxs')
    if os.path.exists(res):
        print("result %s already exists" % res)
        return

    # create events.dat
    from mccomponents.pyre_support.components.DetectorSystemFromXml import merge_and_normalize as mn

    events_outdir = os.path.join(
        workdir, 'work-arcs-neutrons2nxs', 'todetsys', 'out')
    fn = 'events.dat'
    events_path = os.path.join(events_outdir, fn)
    print("* creating %s ..." % (events_path,))
    mn(outputdir=events_outdir, overwrite_datafiles = False)

    # convert events.dat to nexus file
    cmd = "mcvine instruments arcs events2nxs --tofbinsize 0.1 --type raw --Ei 100 %s %s" % (events_path, os.path.join(workdir, 'arcs-sim.nxs'))
    print("* running %s ..." % cmd)
    if os.system(cmd):
        # raise RuntimeError("%s failed" % cmd)
        print("%s failed" % cmd)
        return 1

    import subprocess as sp
    cmd = 'make arcs-sim-wEiData.nxs'
    print("* running %s at %s ... " % (cmd, workdir))
    args = cmd.split()
    p = sp.Popen(args, cwd=workdir)
    if p.wait():
        # raise RuntimeError("%s failed" % cmd)
        print("%s failed" % cmd)
        return 1
    return

if __name__ == '__main__':
    workdir = sys.argv[1]
    run(workdir)
