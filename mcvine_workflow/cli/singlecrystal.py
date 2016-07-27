# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#


import os, stat, click

from . import workflow

"""
angles: -50,40.1,.5
filename_pattern: reduced_%(angle)s.nxs
lattice: 8.87, 8.87, 5.2, 90, 90, 90
orientation:
 u: 1, 0, 0
 v: 0, 1, 0
"""

@workflow.command()
@click.option("--type", default='DGS')
@click.option("--instrument", default='ARCS')
@click.option("--beam", default='')
@click.option("--material", default='V')
@click.option("--excitation", default='spinwave')
@click.option("--scan", default="scan.yml")
def singlecrystal(
        type, instrument,
        beam, 
        material, excitation,
        scan):
    workdir = workdir or "mcvine-workflow-singlecrystal-%s-%s" % (instrument, material)
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

from .powder import create_beam_run_script

# End of file 
