# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating spinwave sample
"""

import os, numpy as np

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
    u, v = uv
    ez = np.dot(h2Q, u); ez/=np.linalg.norm(ez)
    ex1 = np.dot(h2Q, v)
    ey = np.cross(ez, ex1); ey/=np.linalg.norm(ey)
    ex = np.cross(ey, ez)
    R = np.array([ ex, ey, ez ])
    Rflat = R.copy(); Rflat.shape = -1,
    orientation=','.join(str(e) for e in Rflat)
    #  write
    path = os.path.join(outdir, '%s-scattterer.xml' % name)
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


def reciprocal_basis(basis):
    a1,a2,a3 = basis
    v = np.dot(a1, np.cross(a2,a3))
    b1 = np.cross(a2,a3)/v
    b2 = np.cross(a3,a1)/v
    b3 = np.cross(a1,a2)/v
    return np.array([b1,b2,b3])*2*np.pi


def writeXYZ(path, basis, atoms):
    stream = open(path, 'wt')
    stream.write('%s\n' % sum(atoms.values()))
    stream.write('\t'.join(['%s %s %s' % tuple(v) for v in basis]) + '\n')
    for symbol, number in atoms.items():
        for i in range(number):
            stream.write("%s\t0 0 0\n" % symbol)
            continue
        continue
    return

def decode_chemicalformula(formula):
    """given a str like Fe3Al, return a dictionary {'Fe':3, 'Al': 1}
    """
    import re
    l = re.findall('([A-Z][a-z]?)(\d)?', formula)
    d = dict()
    for symbol, n in l:
        d[symbol] = int(n) if n else 1
        continue
    return d

def decode_chemicalformula_using_chemcalc_org(formula):
    import urllib, urllib2
    import json
    ccurl = 'http://www.chemcalc.org/chemcalc/mf'
    # Define a molecular formula string
    # Define the parameters and send them to Chemcalc
    params = {'mf': mf,'isotopomers':'jcamp,xy'}
    response = urllib2.urlopen(ccurl, urllib.urlencode(params))
    # Read the output and convert it from JSON into a Python dictionary
    jsondata = response.read()
    data = json.loads(jsondata)
    atoms = data['parts'][0]['ea']
    for atom in atoms:
        print atom['element']
        print atom['number']
        continue
    return

# End of file 
