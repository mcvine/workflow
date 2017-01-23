# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

sample_yml_example = """
name: sample
chemical_formula: K2V3O8
lattice: 
 constants: 8.87, 8.87, 5.2, 90, 90, 90
 basis_vecotrs:
  - 8.87, 0, 0
  - 0, 8.87, 0
  - 0, 0, 5.2
excitation:
 type: spinwave
 E_Q: 2.563*sqrt(1-(cos(h*pi)*cos(k*pi))**2)
 S_Q: 1
 Emax: 3
orientation:
 u: 1, 0, 0
 v: 0, 1, 0
shape: block width="4.6*cm" height="4.6*cm" thickness="2.3/4*cm"
temperature: 300*K
"""

import os, stat, click

from . import workflow

@workflow.command(help="Create mcvine single crystal workflow")
@click.option("--outdir", default='sim')
@click.option("--type", default='DGS')
@click.option("--instrument", default='ARCS')
@click.option("--sample", default='sample.yml')
@click.option('--beam2sample', default=None)
@click.option("--ncount", default=1e7)
@click.option("--buffer_size", default=0)
@click.option("--nodes", default=10)
def singlecrystal(outdir, type, instrument, sample, beam2sample, ncount, buffer_size, nodes):
    if beam2sample is None:
        beam2sample = beam2sample_dict.get(instrument.lower())
        if beam2sample is None:
            raise RuntimeError("Please specify beam2sample (meters")
    # create outdir
    if os.path.exists(outdir):
        raise IOError('%s already exists' % outdir)
    os.makedirs(outdir)
    from mcvine import resources
    from mcvine_workflow import root
    # by copying from template
    template = os.path.join(root, type, 'generic', 'single-crystal')
    from .._shutil import rsync
    rsync(template, outdir)
    # create "beam" subdir
    beam = os.path.join(outdir, 'beam')
    os.makedirs(beam)
    # add script to run beam
    create_beam_run_script(beam, instrument.lower())
    # copy sampleassembly template
    if sample.endswith(".yml"):
        # load sample configuration from yml
        from ..sample import loadSampleYml
        sample = loadSampleYml(sample)
        # create sample assembly using scaffolding
        from ..singlextal.scaffolding import createSampleAssembly
        createSampleAssembly(os.path.join(outdir, 'sampleassembly'), sample)
    else:
        if os.path.isabs(sample) and os.path.isdir(sample):
            # this means "sample" is a path to a sample assembly diretory
            srcpath = ssample
        else:
            # this means "sample" is an ID with which we can look up a sample
            # example directory in the mcvine resources
            sampleargs = sample.split('/')
            if len(sampleargs) > 3:
                raise ValueError('Wrong sample input %s. Examples: %s' % (sample, sample_examples))
            template = resources.sample(*sampleargs)
            if not os.path.exists(template):
                raise RuntimeError("Sample template for %r does not exist" % sample)
            srcpath = template
        # copying
        rsync(srcpath, os.path.join(outdir, 'sampleassembly'))
    # fix Makefile and sss.pml
    d = dict(locals()); d['instrument'] = instrument.lower()
    _fix_using_template(os.path.join(outdir, 'scattering', 'template', 'Makefile'), d)
    _fix_using_template(os.path.join(outdir, 'scattering', 'template', 'sss.pml'), d)
    _fix_using_template(os.path.join(outdir, 'scattering', 'sim.yml'), d)
    return

from .powder import beam2sample_dict, create_beam_run_script, _fix_using_template

sample_examples = '"V", "V/300K", or "V/300K/plate"'


# End of file 
