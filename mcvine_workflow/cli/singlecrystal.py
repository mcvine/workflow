# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#


import os, stat, click

from . import workflow

@workflow.command()
@click.option("--type", default='DGS')
@click.option("--instrument", default='ARCS')
@click.option("--beam", default='')
@click.option("--sample", default='V')
@click.option("--workdir", default="")
def singlecrystal(type, instrument, beam, sample, workdir):
    workdir = workdir or "mcvine-workflow-powder-%s-%s" % (instrument, sample)
    # create workdir
    if os.path.exists(workdir):
        raise IOError('%s already exists' % workdir)
    os.makedirs(workdir)
    # create a symbolic link to the beam
    # beam and sampleassembly should be symlinks
    # should modify template Makefile to create symlinks 
    # to beam and sampleassembly
    # this way when staging we can use rsync -avzL
    # and the beam and sampleassembly symlinks in the 
    # work-<psi> dirs will be created on the fly.
    # copy from template
    from mcvine import resources
    from mcvine_workflow import root
    template = os.path.join(root, type, instrument, 'powder')
    import shutil
    shutil.copytree(template, workdir)
    # create "beam" subdir
    beam = os.path.join(workdir, 'beam')
    os.makedirs(beam)
    # add script to run beam
    create_beam_run_script(beam, instrument.lower())
    # copy sampleassembly template
    sampleargs = sample.split('/')
    if len(sampleargs) > 3:
        raise ValueError('Wrong sample input %s. Examples: %s' % (sample, sample_examples))
    template = resources.sample(*sampleargs)
    if not os.path.exists(template):
        raise RuntimeError("Sample template for %r does not exist" % sample)
    shutil.copytree(template, os.path.join(workdir, 'sampleassembly'))
    return


sample_examples = '"V", "V/300K", or "V/300K/plate"'


def create_beam_run_script(workdir, instrument):
    name = "run-beam.sh"
    content = """#!/usr/bin/env bash

mcvine instruments %s beam --keep-in-cache --use-cache -E=100 --ncount=1e8

""" % instrument
    path = os.path.join(workdir, name)
    open(path, 'wt').write(content)
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)
    return


# End of file 
