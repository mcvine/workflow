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
        chemical_formula=None, E_Q=None, S_Q='1', Emax="{Emax}"):
    """
    Inputs
    - name: name of sample
    - lattice_basis: a1, a2, a3 basis vectors
    - uv: u,v vectors
    - E_Q: E(vector Q) expression
    - S_Q: S(vector Q) expression
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
    writeXYZ(xyzpath, lattice_basis, atoms)
    # scatterer.xml
    reci_basis = reciprocal_basis(lattice_basis)
    #  Q = [b1 b2 b3]/ROW dot [h k l]/COL = h2Q dot [h k l]/COL
    #  so h2Q = [b1 b2 b3]/ROW
    h2Q = reci_basis.T
    Q2h = np.linalg.inv(h2Q)
    #  hkl
    h_expr = "%s*Qx+%s*Qy+%s*Qz" % tuple(Q2h[0])
    k_expr = "%s*Qx+%s*Qy+%s*Qz" % tuple(Q2h[1])
    l_expr = "%s*Qx+%s*Qy+%s*Qz" % tuple(Q2h[2])
    #  orientation
    orientation=computeOrientationStr(uv=uv, h2Q=h2Q)
    #  write
    path = os.path.join(outdir, '%s-scatterer.xml' % name)
    open(path, 'wt').write(scatterer_template % locals())
    return


scatterer_template = """<?xml version="1.0"?>

<!DOCTYPE scatterer>

<!-- weights: absorption, scattering, transmission -->
<homogeneous_scatterer 
  mcweights="0, 1, 0.1"
  max_multiplescattering_loops="3"
  >
  
  <KernelContainer average="yes">
    
    <!-- a simple kernel for elastic scattering. more realistic kernel exists. -->
    <E_Q_Kernel 
	E_Q="1" 
	S_Q="1"
	Qmin="0./angstrom"
	Qmax="16./angstrom"
	/>
    
    <!-- kernel for spin wave
      E_Q: expression for E(Q)
      S_Q: expression for E(Q)
      Emax: set this to maximum energy of the spin-wave excitation to help speed up the sim.
      orientation: flattened rotation matrix M. M dot Q_crystal = Q_instrument
     -->
    <E_vQ_Kernel 
	E_Q="pi:=3.1415926535897932; twopi:=2*pi; 
             h:=%(h_expr)s;
             k:=%(k_expr)s;
             l:=%(l_expr)s;
             %(E_Q)s"
	S_Q="pi:=3.1415926535897932; twopi:=2*pi; 
             h:=%(h_expr)s; 
             k:=%(k_expr)s; 
             l:=%(l_expr)s;
             %(S_Q)s"
	Emax="%(Emax)s*meV"
        orientation="%(orientation)s"
	/>
    
  </KernelContainer>
  
</homogeneous_scatterer>
"""

# End of file 
