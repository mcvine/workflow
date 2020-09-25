# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

from future.standard_library import install_aliases
install_aliases()
import os, numpy as np

def computeOrientationStr(lattice_basis=np.eye(3), uv=([1,0,0], [0,1,0]), h2Q=None):
    """
    Inputs
    - lattice_basis: a1, a2, a3 basis vectors
    - uv: u,v vectors
    Outputs
    - kernel orientation str
    """
    if h2Q is None:
        reci_basis = reciprocal_basis(lattice_basis)
        #  Q = [b1 b2 b3]/ROW dot [h k l]/COL = h2Q dot [h k l]/COL
        #  so h2Q = [b1 b2 b3]/ROW
        h2Q = reci_basis.T
    #  orientation
    u, v = uv
    ez = np.dot(h2Q, u); ez/=np.linalg.norm(ez)
    ex1 = np.dot(h2Q, v)
    ey = np.cross(ez, ex1); ey/=np.linalg.norm(ey)
    ex = np.cross(ey, ez)
    R = np.array([ ex, ey, ez ])
    Rflat = R.copy(); Rflat.shape = -1,
    orientation=','.join(str(e) for e in Rflat)
    return orientation


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
    import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
    import json
    ccurl = 'http://www.chemcalc.org/chemcalc/mf'
    # Define a molecular formula string
    # Define the parameters and send them to Chemcalc
    params = {'mf': mf,'isotopomers':'jcamp,xy'}
    response = urllib.request.urlopen(ccurl, urllib.parse.urlencode(params))
    # Read the output and convert it from JSON into a Python dictionary
    jsondata = response.read()
    data = json.loads(jsondata)
    atoms = data['parts'][0]['ea']
    for atom in atoms:
        print(atom['element'])
        print(atom['number'])
        continue
    return

# End of file 
