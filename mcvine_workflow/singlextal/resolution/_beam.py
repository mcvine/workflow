# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import os

def computeEi_and_t0(beampath, instrument='ARCS'):
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
    print computeEi_and_t0(beam)
    return

if __name__ == '__main__': test()

# End of file 
