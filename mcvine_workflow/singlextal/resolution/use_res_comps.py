# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
Inputs

* sample assembly
  - shape
  - material (??.xyz)
  - pixel position
  - pixel radius
  - tof at pixel
  - dtof
* beam_path
  - a quick simulation to generate event nexus file and let mantid compute t0 and Ei?
    - t0
    - Ei
* dynamics
  - E
  - hkl
  - sample.yml
  - from these compute Q in instrument coordinate system (z vertical up)
    and also hkl2Q matrix
* L_m2s
* pixel_pos (this was calculated using R=3, cylinder)
* pixel_pressure, radius, height
* distance from saved neutrons to sample position
* Nbuffer
"""

import os, numpy as np
from mcni.utils import conversion as Conv


def setup(sampleyml, beam, E, hkl, psi_axis, instrument, pixel):
    # load beam
    from ._beam import computeEi_and_t0
    Ei, t0 = computeEi_and_t0(beam, instrument.name)
    # load sample
    from mcvine.cli.config import loadYmlConfig
    sample = loadYmlConfig(sampleyml)
    # the sample kernel need information of E and hkl
    Q, hkl2Qmat = calcQ(sampleyml, Ei, E, hkl, psi_axis, Npsisegments=10)
    # import pdb; pdb.set_trace()
    kfv, Ef = computeKf(Ei, E, Q)
    pixel_position = computePixelPosition(kfv, instrument)
    # at this point the coordinates have convention of z vertical up
    # ** coordinate system for calculated position: z is vertical **
    # compute nominal tof from mod to sample
    vi = Conv.e2v(Ei)
    t_m2s = instrument.L_m2s/vi + t0*1e-6
    # nominal tof from mod to pixel
    vf = Conv.e2v(Ef)
    t_s2p = np.linalg.norm(pixel_position)/vf
    t_m2p = t_m2s + t_s2p
    print "t_m2s=%s, t_s2p=%s, t_m2p=%s" % (t_m2s, t_s2p, t_m2p)
    return

def computeKf(Ei, E, Q):
    ki = Conv.e2k(Ei);
    print "ki=%s" % (ki,)
    kiv = np.array([ki, 0, 0])
    kfv = kiv - Q
    print "vectors ki=%s, kf=%s" % (kiv, kfv)
    Ef = Ei - E
    # ** Verify the momentum and energy transfers **
    print "These two numbers should be very close:"
    print Ei-Conv.k2e(np.linalg.norm(kfv))
    print Ei-Ef
    assert np.isclose(Ef, Conv.k2e(np.linalg.norm(kfv)))
    print "Ei=%s, Ef=%s" % (Ei,Ef)
    return kfv, Ef

def computePixelPosition(kfv, instrument):
    # ** compute nominal TOF at detector pixel **
    # where is detector pixel?
    # cylinder radius = 3meter. 
    t_sample2pixel = instrument.detsys_radius/(kfv[0]**2 + kfv[1]**2)**.5
    pixel_pos = kfv*t_sample2pixel
    print "pixel positon=%s" % (pixel_pos,)
    return pixel_pos

def calcQ(sampleyml, Ei, E, hkl, psi_axis, Npsisegments=10):
    from ..io import loadXtalOriFromSampleYml
    xtalori = loadXtalOriFromSampleYml(sampleyml)
    psimin, psimax, dpsi = psi_axis
    from ..solve_psi import solve
    results = solve(
        xtalori, Ei, hkl, E, psi_min=psimin, psi_max=psimax,
        Nsegments = Npsisegments)
    assert len(results)
    from ...singlextal.coords_transform import hkl2Q
    r0 = results[0]
    psi_in_degrees = r0
    xtalori.psi = r0*np.pi/180.
    Q = hkl2Q(hkl, xtalori) # here the convension is z vertical
    hkl2Qmat = xtalori.hkl2cartesian_mat()
    return Q, hkl2Qmat


def run():
    from mcni.components.NeutronFromStorage import NeutronFromStorage
    source = NeutronFromStorage('source', path=beam_neutrons_path)
    from mccomponents.sample import samplecomponent
    sample = samplecomponent( 'sample', xmlpath)
    from mccomponents.components.DGSSXResPixel import DGSSXResPixel
    pixel = DGSSXResPixel(
        "pixel", 
        pressure=10*101325, tof=t_m2p,
        radius=0.0254/2, height=1./128)
    # build instrument
    import mcni
    instrument = mcni.instrument( [source, sample, pixel] )
    # put components into place
    geometer = mcni.geometer()
    geometer.register( source, (0,0,-0.15), (0,0,0) )
    geometer.register( sample, (0,0,0), (0,0,0) )
    geometer.register( pixel, (pixel_pos[1], pixel_pos[2], pixel_pos[0]), 
                       (0,0,0) )
    # neutron buffer
    from mcni.neutron_storage.idf_usenumpy import count
    N0 = count(beam_neutrons_path)
    Nbuffer = 100000
    # custom tracer
    dxs_all = None; dEs_all = None; probs_all=None
    start = 0
    for i in range(int(np.ceil(N0/Nbuffer))):
    # for i in range(10):
        end = start + Nbuffer
        end = min(end, N0)
        sys.stdout.write("%s-%s: " % (start, end-1)); sys.stdout.flush()
        neutrons = mcni.neutron_buffer(end-start)
        # simulate
        tracer = NeutronTracer()
        mcni.simulate( instrument, geometer, neutrons, tracer=tracer)
        #
        dummy_start, incident, scattered, detected, dummy_end = tracer._store
        is_scattered = incident.v != scattered.v
        is_scattered = np.logical_or(
            is_scattered[:,0],
            np.logical_or(is_scattered[:,1], is_scattered[:,2])
            )
        good = np.logical_and(is_scattered, detected.p>np.finfo(float).eps)

        vi = incident.v[good]
        vf = scattered.v[good]
        probs = p = detected.p[good]

        from mcni.utils import conversion
        Ei = conversion.VS2E * (vi*vi).sum(axis=-1)
        Ef = conversion.VS2E * (vf*vf).sum(axis=-1)
        Es = Ei - Ef

        vQ = vi-vf
        Qs = vQ * conversion.V2K
        Qs = np.array([Qs[:, 2], Qs[:, 0], Qs[:, 1]]).T
        # print Qs
        # print Es
        dQs = Qs - Q
        dEs = Es - E
        Q2hkl = np.linalg.inv(hkl2Q)
        dhkls = np.dot(dQs, Q2hkl)
        # print dhkls
        # print dEs
        # print p
        dxs = np.dot( dhkls, np.array([-1,1,-1])/3. )
        if dxs_all is None:
            dxs_all = dxs
            dEs_all = dEs
            probs_all = probs
        else:
            dxs_all = np.concatenate((dxs_all, dxs))
            dEs_all = np.concatenate((dEs_all, dEs))
            probs_all = np.concatenate((probs_all, probs))
        print
        start = end
        continue
    # reverse x and E
    dxs_all *= -1
    dEs_all *= -1
    np.save("dxs.npy", dxs_all)
    np.save("dEs.npy", dEs_all)
    np.save("probs.npy", probs_all)
    h, xedges, yedges = np.histogram2d(
        dxs_all, dEs_all, bins=100, weights=probs_all)
    xaxis = H.axis('x', boundaries=xedges)
    Eaxis = H.axis('E', boundaries=yedges)
    res = H.histogram('res', (xaxis, Eaxis), data=h)
    hh.dump(res, 'res.h5')
    return


def main():
    # test_process()
    run()
    return


class _N:
    def __init__(self, r, v, p):
        self.r, self.v, self.p = r,v,p
        return

from mcni.pyre_support.AbstractNeutronTracer import AbstractNeutronTracer
class NeutronTracer(AbstractNeutronTracer):

    def __init__(self, name='neutron-tracer'):
        super(NeutronTracer, self).__init__(name)
        self._store = []
        return

    
    def __call__(self, neutrons, context=None):
        if context:
            context.identify(self)

        if self._process:
            from mcni.neutron_storage import neutrons_as_npyarr
            a = neutrons_as_npyarr(neutrons)
            a.shape = -1, 10
            r = a[:, :3]
            v = a[:, 3:6]
            p = a[:, -1]
            self._store.append(_N(r, v, p))
        sys.stdout.write(".")
        sys.stdout.flush()
        return


    def onBefore(self, context):
        self._process = False


    def onProcessed(self, context):
        self._process = True


# End of file 
