# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for create single crystal samples for mcvine sample assembly.
"""

import os

def createSampleAssembly(outdir, sample, **kwds):
    """
    * outdir: output directory
    * sample: sample object. can be constructed from yaml file
              using mcvine.workflow.sample.loadSampleYml
              Example yaml file: tests/DGS/ARCS/Si.yml
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # get sample data
    sample_dict = sample.__dict__.copy()
    # format shape
    sample_dict['shape'] = _format_shape(sample_dict['shape'])
    # sampleassembly.xml
    content = sampleassembly_template % sample_dict
    open(os.path.join(outdir, 'sampleassembly.xml'), 'wt').write(content)
    # sample
    if sample.orientation:
        so = sample.orientation
        uv = so.u, so.v
    else:
        uv = None
    from .sample import createSample
    createSample(
        outdir, name=sample.name, 
        lattice_basis=sample.lattice.basis_vectors, uv=uv,
        chemical_formula=sample.chemical_formula,
        excitations = sample.excitations,
        lattice_primitive_basis=sample.lattice.primitive_basis_vectors,
        **kwds
        )
    return


def _format_shape(shape):
    indent = 6 * ' '
    # shape is an xml string
    if shape.startswith('<'):
        return '\n'.join( indent + x for x in shape.splitlines() )
    # shape is a simple oneliner that can convert to a xml tag
    if '\n' not in shape:
        return '%s<%s />' % (indent, shape)
    # yml shape specification
    raise NotImplementedError


sampleassembly_template = """<?xml version="1.0"?>

<!DOCTYPE SampleAssembly>

<SampleAssembly name="X"
   max_multiplescattering_loops_among_scatterers="1"
   max_multiplescattering_loops_interactM_path1="4"
   min_neutron_probability=".1"
 >
  
  <PowderSample name="%(name)s" type="sample">
    <Shape>
%(shape)s
    </Shape>
    <Phase type="crystal">
      <ChemicalFormula>%(chemical_formula)s</ChemicalFormula>
      <xyzfile>%(name)s.xyz</xyzfile>
    </Phase>
  </PowderSample>
  
  <LocalGeometer registry-coordinate-system="InstrumentScientist">
    <Register name="%(name)s" position="(0,0,0)" orientation="(0, 0, 0)"/>
  </LocalGeometer>

  <Environment temperature="%(temperature)s"/>

</SampleAssembly>
"""
# End of file 
