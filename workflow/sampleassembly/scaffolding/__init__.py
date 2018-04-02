# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for create single crystal samples for mcvine sample assembly.
"""

import os

def createSampleAssembly(outdir, sample, *scatterers, **kwds):
    """
    * outdir: output directory
    * sample: sample object. can be constructed from yaml file
              using mcvine.workflow.sample.loadSampleYml
              Example yaml file: tests/DGS/ARCS/Si.yml
    * scatterers: scatterers in addition to sample, such as sample environment
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    scatterers = [sample] + list(scatterers)
    # sampleassembly.xml
    from .sampleassembly_xml import create
    content = create(scatterers)
    open(os.path.join(outdir, 'sampleassembly.xml'), 'wt').write(content)
    for scatterer in scatterers:
        # scatterer
        if scatterer.orientation:
            so = scatterer.orientation
            uv = so.u, so.v
        else:
            uv = None
        from .sample import createSample
        createSample(
            outdir, name=scatterer.name, 
            lattice_basis=scatterer.lattice.basis_vectors, uv=uv,
            chemical_formula=scatterer.chemical_formula,
            excitations = scatterer.excitations,
            lattice_primitive_basis=scatterer.lattice.primitive_basis_vectors,
            **kwds
            )
    return


# End of file 
