#!/usr/bin/env python

import os, subprocess as sp

def run(angle, target=None):
    target = target or "arcs-sim-wEiData.nxs"
    print angle
    work = 'work_%s' % angle
    cmd = 'cp -a template %s' % work
    if not os.path.exists(work) :
        if os.system(cmd):
            print "*** %s failed" % cmd
            return
    cmd = ['make', target, 'SAMPLE_ANGLE=%s' % angle]
    print ' '.join(cmd)
    logfile = open(os.path.join(work, "log.run_oneangle.%s" % target), 'w')
    p = sp.Popen(cmd, stdout=logfile, stderr=logfile, cwd=work)
    if p.wait():
        print "*** %s failed" % (' '.join(cmd),)
    return


if __name__ == '__main__':
    import sys
    angle = sys.argv[1]
    target = None
    if len(sys.argv) == 3: target = sys.argv[2]
    run(angle, target)
