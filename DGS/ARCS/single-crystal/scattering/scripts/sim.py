#!/usr/bin/env python

import os, subprocess as sp, sys, numpy as np

curdir = os.path.abspath(os.path.dirname(__file__))
if curdir not in sys.path:
    sys.path.insert(0, curdir)


import click


@click.command()
@click.option("--angles", default=None)
@click.option("--angle", default=None)
@click.option("--config", default="sim.yml")
@click.option("--target", default="event-nxs")
def main(angles, angle, config, target):
    from config import loadYmlConfig
    config = loadYmlConfig(config)
    envvars = dict(
        INSTRUMENT=config.instrument.name,
        NCOUNT=config.scatter.ncount,
        MS=config.scatter.multiple_scattering,
        NODES=config.cluster.nodes,
        )
    if angles is not None and angle is not None:
        raise ValueError("Both angles and angle were provided")
    if angle is not None:
        angles = [angle]
    else:
        env = dict(arange=np.arange)
        angles = eval(angles, env)
    for angle in angles:
        run_oneangle(angle, config, envvars, target)
    return


def run_oneangle(angle, config, envvars, target):
    # create working dir
    work = 'work_%s' % angle
    if not os.path.exists(work) :
        cmd = 'cp -a %s %s' % (config.scatter.template, work)
        if os.system(cmd):
            print "*** %s failed" % cmd
            return
    # run
    cmd = ['make', target]
    cmd += ['%s=%s' % (k,v) for k,v in envvars.iteritems()]
    cmd.append('SAMPLE_ANGLE=%s' % angle)
    cmd = ' ' .join(cmd)
    save = os.path.abspath(os.curdir)
    os.chdir(work)
    if os.system(cmd):
        print "*** %s failed" % cmd
    os.chdir(save)
    return


if __name__ == '__main__': main()
