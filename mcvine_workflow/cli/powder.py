# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#


import os, stat, click

from . import workflow

@workflow.command(help="Create mcvine powder workflow")
@click.option("--type", default='DGS')
@click.option("--instrument", default='ARCS')
@click.option("--sample", default='V')
@click.option("--workdir", default="")
@click.option("--ncount", default=1e7)
@click.option("--buffer_size", default=100000)
@click.option("--nodes", default=10)
@click.option("--qaxis", default="0 15 0.1")
@click.option('--mod2sample', default=None)
def powder(type, instrument, sample, workdir, ncount, buffer_size, nodes, qaxis, mod2sample):
    workdir = workdir or "mcvine-workflow-powder-%s-%s" % (instrument, sample)
    if mod2sample is None:
        mod2sample = mod2sample_dict.get(instrument.lower())
        if mod2sample is None:
            raise RuntimeError("Please specify mod2sample (meters")
    # copy from template
    from mcvine import resources
    from mcvine_workflow import root
    template = os.path.join(root, type, 'generic', 'powder')
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
    # fix Makefile and sss.pml
    d = dict(locals()); d['instrument'] = instrument.lower()
    _fix_using_template(os.path.join(workdir, 'Makefile'), d)
    _fix_using_template(os.path.join(workdir, 'sss.pml'), d)
    return

mod2sample_dict = dict(
    arcs = '0.15',
    seq = '0.15',
    cncs = '0.15',
    )


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


def _fix_using_template(path, params):
    template = open(path).read()
    new = template % params
    open(path, 'wt').write(new)
    return


# End of file 
