#!/usr/bin/env python

import numpy as np, os

def main():
    from rescue_detsim import run
    failed = []
    for sample in np.arange(-5,90.1,0.5):
        work = 'work_%s' % sample
        if run(work):
            failed.append(work)
        continue
    
    print "Failed:"
    for w in failed:
        print " - %s" % w
    return

if __name__ == '__main__' : main()

