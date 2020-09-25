#!/usr/bin/env python

import os, subprocess as sp, sys

curdir = os.path.abspath(os.path.dirname(__file__))
if curdir not in sys.path:
    sys.path.insert(0, curdir)


import click


@click.command()
@click.argument("angle")
@click.option("--config", default="sim.yml")
@click.option("--target", default="event-nxs")
def main(angle, config, target):
    from config import loadYmlConfig
    config = loadYmlConfig(config)
    envvars = dict(
        INSTRUMENT=config.instrument.name,
        NCOUNT=config.scatter.ncount,
        MS=config.scatter.multiple_scattering,
        NODES=config.cluster.nodes,
        SAMPLE_ANGLE=angle,
        )
    # create working dir
    work = 'work_%s' % angle
    if not os.path.exists(work) :
        cmd = 'cp -a %s %s' % (config.scatter.template, work)
        if os.system(cmd):
            print("*** %s failed" % cmd)
            return
    # run
    cmd = ['make', target]
    cmd += ['%s=%s' % (k,v) for k,v in envvars.items()]
    cmd = ' ' .join(cmd)
    os.chdir(work)
    if os.system(cmd):
        print("*** %s failed" % cmd)
        return
    return


if __name__ == '__main__': main()
