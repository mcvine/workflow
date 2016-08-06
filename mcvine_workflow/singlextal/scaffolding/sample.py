# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating spinwave sample
"""

import os, numpy as np
from .utils import computeOrientationStr, reciprocal_basis, writeXYZ, decode_chemicalformula

def createSample(
        outdir, name=None, 
        lattice_basis=np.eye(3), uv=([1,0,0], [0,1,0]),
        chemical_formula=None, 
        excitations = None,
        lattice_primitive_basis=None,
        add_elastic_line = True,
        ):
    """
    Inputs
    - name: name of sample
    - lattice_basis: a1, a2, a3 basis vectors
    - uv: u,v vectors
    - kernels: a list of kernels
    Outputs
    - SAMPLE.xyz
    - SAMPLE-scatterer.xml with correct orientation
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not name: 
        name = chemical_formula
    # xyz
    xyzpath = os.path.join(outdir, '%s.xyz' % name)
    atoms = decode_chemicalformula(chemical_formula)
    if lattice_primitive_basis:
        writeXYZ(xyzpath, lattice_primitive_basis, atoms)
    else:
        writeXYZ(xyzpath, lattice_basis, atoms)
    # scatterer.xml
    reci_basis = reciprocal_basis(lattice_basis)
    #  Q = [b1 b2 b3]/ROW dot [h k l]/COL = h2Q dot [h k l]/COL
    #  so h2Q = [b1 b2 b3]/ROW
    h2Q = reci_basis.T
    #  orientation
    orientation=computeOrientationStr(uv=uv, h2Q=h2Q)
    # prepare kernels
    kernels = makeKernels(excitations, h2Q, orientation, add_elastic_line=add_elastic_line)
    #  write
    path = os.path.join(outdir, '%s-scatterer.xml' % name)
    open(path, 'wt').write(scatterer_template % locals()) 
    return


def makeKernels(excitations, hkl, orientation, add_elastic_line=True):
    ks = []
    types = [e.type for e in excitations]
    # if 'phonon' not in types:
    # XXX hack
    if add_elastic_line:
        ks.append(simple_elastic_kernel)
    for excitation in excitations:
        ks.append(makeKernel(excitation, hkl, orientation))
        continue
    return '\n'.join(ks)


from . import spinwave, phonon, deltafunction
def makeKernel(excitation, hkl, orientation):
    type = excitation.type
    mod = globals()[type]
    return mod.createKernel(excitation, hkl, orientation)


scatterer_template = """<?xml version="1.0"?>

<!DOCTYPE scatterer>

<!-- weights: absorption, scattering, transmission -->
<homogeneous_scatterer 
  mcweights="0, 1, 0.1"
  max_multiplescattering_loops="3"
  >
  
  <KernelContainer average="yes">

%(kernels)s
    
  </KernelContainer>
  
</homogeneous_scatterer>
"""

simple_elastic_kernel = """
    <!-- a simple kernel for elastic scattering. more realistic kernel exists. -->
    <E_Q_Kernel 
	E_Q="1" 
	S_Q="1"
	Qmin="0./angstrom"
	Qmax="16./angstrom"
	/>
""" 
# End of file 
