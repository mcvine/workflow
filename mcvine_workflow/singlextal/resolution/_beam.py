# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import os, numpy as np


def computeEi_and_t0(beampath, instrument):
    """use Ei saved in props.json. use saved neutrons information to compute t0
    """
    Ei = getEi(beampath)
    
    import mcni.neutron_storage as ns
    neutrons = ns.readneutrons_asnpyarr(os.path.join(beampath, 'out', 'neutrons'))
    assert neutrons.shape[-1] == 10
    t = neutrons[:, -2]
    vz = neutrons[:, 5]
    from mcni.units import parser; parser = parser()
    z_beam = parser.parse(instrument.L_m2s) + parser.parse(instrument.offset_sample2beam)
    z_beam /= parser.parse('meter')
    z = neutrons[:, 2] + z_beam
    t0 = t - z/vz
    # take histogram
    h, tbb = np.histogram(t0, bins=200)
    # compute t0 with maximum intensity
    t0_max_int = tbb[np.argmax(h)]
    # only retain a small portion of the whole t0 histogram
    t0a = t0[t0<t0_max_int + np.std(t0)]
    # now compute the histogram of the subset
    h, tbb = np.histogram(t0a, bins=200)
    tcenters = (tbb[:-1]+tbb[1:])/2
    # fit to gaussian
    from scipy.optimize import curve_fit
    def gaus(x,a,x0,sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))
    p0=[np.max(h), tcenters[np.argmax(h)], np.abs(np.median(t0a)-np.average(t0a))]
    popt,pcov = curve_fit(gaus, tcenters, h, p0=p0)
    t0 = popt[1]
    print Ei, t0
    return Ei, t0


def getEi(beampath):
    import json, os
    beam_outdir = os.path.join(beampath, 'out')
    props_path = os.path.join(beam_outdir, 'props.json')
    s = open(props_path).read()
    s = s.replace("'", '"') # ' -> "
    props = json.loads(s)
    Ei, unit = props['average energy'].split()
    return float(Ei)


def computeEi_and_t0_usingMantid_ARCS(beampath, instrument='ARCS'):
    """use mantid to compute Ei and t0
    """
    # only implementation right now
    assert instrument=='ARCS'
    # create dummy nxs
    import hashlib
    key = hashlib.sha224(beampath).hexdigest()
    outdir = 'computeEi_and_t0-%s' % key
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    dummynxs = os.path.join(outdir, 'dummy.nxs')
    if not os.path.exists(dummynxs):
        create_dummy_nxs(dummynxs, beampath)
    results = os.path.join(outdir, 'results.txt')
    if not os.path.exists(results):
        # call mantid
        from mantid import simpleapi as mtdsa
        ws = mtdsa.Load(dummynxs, LoadMonitors=True)
        Ei, firstMonitorPeak, FirstMonitorIndex, t0 = mtdsa.GetEi(ws[1])
        open(results, 'wt').write('%s,%s' % (Ei,t0))
    else:
        Ei,t0 = eval(open(results).read().strip())
    return Ei, t0

def create_dummy_nxs(out, beam):
    import shutil, sys
    from mcvine.instruments.ARCS.nxs.raw import nxs_template, populateEiData
    shutil.copyfile(nxs_template, out)
    import time; time.sleep(0.5)
    import h5py
    f = h5py.File(out, 'a')
    entry = f['entry']
    populateEiData(entry, os.path.join(beam, 'out'))
    return out

def test():
    beam = "/SNS/users/lj7/simulations/ARCS/beam/100meV-n1e10"
    Ei,t0 = computeEi_and_t0(beam)
    assert np.isclose(Ei, 100.482385711)
    assert np.isclose(t0, 18.7623408857)
    return

if __name__ == '__main__': test()

# End of file 
