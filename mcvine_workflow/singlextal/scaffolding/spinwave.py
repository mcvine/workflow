# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Tools for creating spinwave sample
"""

import os

def createSample(outdir, name, xtalori, chemical_formula=None, E_Q=None, S_Q='1'):
    """
    Inputs
    - name: name of sample
    - xtalori: crytal orientation (singlextal.XtalOrientation.XtalOrientation) instance
    - E_Q: E(vector Q) expression
    - S_Q: S(vector Q) expression
    Outputs
    - SAMPLE.xyz
    - SAMPLE-scatterer.xml with correct orientation
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # xyz
    xyzpath = os.path.join(outdir, '%s.xyz' % name)
    chemical_formula = name if not chemical_formula
    print decode_chemicalformula(chemical_formula)
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
