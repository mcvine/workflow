# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for create single crystal samples for mcvine sample assembly.
"""

import os

def createSampleAssembly(outdir, sample):
    """
    * outdir: output directory
    * sample: sample object. can be constructed from yaml file. 
              Example yaml file: tests/DGS/ARCS/Si.yml
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # sampleassembly.xml
    content = sampleassembly_tempalte % sample.__dict__
    open(os.path.join(outdir, 'sampleassembly.xml'), 'wt').write(content)
    # sample files
    bv = map(eval, sample.lattice.basis_vectors)
    if hasattr(sample.lattice, "primitive_basis_vectors"):
        pbv = map(eval, sample.lattice.primitive_basis_vectors)
    else:
        pbv = None
    so = sample.orientation
    uv = map(eval, (so.u, so.v))
    excitations = getattr(sample, 'excitations', [])
    excitation = getattr(sample, 'excitation', None)
    if excitation is not None:
        excitations.append(excitation)
    from .sample import createSample
    createSample(
        outdir, name=sample.name, 
        lattice_basis=bv, uv=uv,
        chemical_formula=sample.chemical_formula,
        excitations = excitations,
        lattice_primitive_basis=pbv
        )
    return

sampleassembly_tempalte = """<?xml version="1.0"?>

<!DOCTYPE SampleAssembly>

<SampleAssembly name="X"
   max_multiplescattering_loops_among_scatterers="1"
   max_multiplescattering_loops_interactM_path1="4"
   min_neutron_probability=".1"
 >
  
  <PowderSample name="%(name)s" type="sample">
    <Shape>
      <%(shape)s />
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
