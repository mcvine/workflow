#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal import dynrange
from mcvine_workflow.sample import loadSampleYml
from mcvine_workflow.DGS import ARCS
from matplotlib import pyplot as plt

import numpy as np, os

thisdir = os.path.dirname(__file__)
sample_yml_path = os.path.join(thisdir, "..", "..", 'DGS', 'ARCS', 'Si.yml')
outdir = "_tmp.dynrange"
if not os.path.exists(outdir):
    os.makedirs(outdir)

def test_iterPointsInSlice():
    sample = loadSampleYml(sample_yml_path)
    psilist = np.arange(-5, 90., 0.5)
    Ei = 100.
    hkl0 = [-16/3., -8/3., 8/3.]
    hkl_dir = [-1., 1., -1.]
    xaxis = np.arange(-6, 6, .1)
    plt.figure()
    for psi, xs, Es in dynrange.iterPointsInSlice(
            sample, psilist, Ei, hkl0, hkl_dir, xaxis,
            ARCS.scattering_angle_constraints):
        plt.plot(xs, Es, label=str(psi))
        continue
    plt.savefig(os.path.join(outdir, "dynrange.slice_111.png"))
    return


def test_plotDynRangeOfSlice():
    sample = loadSampleYml(sample_yml_path)
    psilist = np.arange(-5, 90., 0.5)
    Ei = 100.
    hkl0 = [-16/3., -8/3., 8/3.]
    hkl_dir = [-1., 1., -1.]
    xaxis = np.arange(-6, 6, .1)
    plt.figure()
    dynrange.plotDynRangeOfSlice(
        sample, psilist, Ei, hkl0, hkl_dir, xaxis,
        ARCS.scattering_angle_constraints,
        Erange=(-5, 80))
    plt.savefig(os.path.join(outdir, "dynrange.slice_111_2.png"))
    return

def test_plotDynRangeOfSlice2():
    sample = loadSampleYml(sample_yml_path)
    psilist = np.arange(-5, 90., 0.5)
    Ei = 100.
    hkl0 = [0,0,0]
    hkl_dir = [1., 0., 0.]
    xaxis = np.arange(-12, 6, .1)
    plt.figure()
    dynrange.plotDynRangeOfSlice(
        sample, psilist, Ei, hkl0, hkl_dir, xaxis,
        ARCS.scattering_angle_constraints,
        Erange=(-5, 80))
    plt.savefig(os.path.join(outdir, "dynrange.slice_100_from000.png"))
    return

def test_plotDynRangeOfSlices():
    sample = loadSampleYml(sample_yml_path)
    psilist = np.arange(-5, 90., 0.5)
    Ei = 100.
    hkl0s = [[0,k,l] for k in range(-3, 3)
             for l in range(-3,3)]
    hkl_dir = [1., 0, 0]
    xaxis = np.arange(-6, 6, .1)
    for hkl0 in hkl0s:
        plt.figure()
        dynrange.plotDynRangeOfSlice(
            sample, psilist, Ei, hkl0, hkl_dir, xaxis,
            ARCS.scattering_angle_constraints,
            Erange=(-5, 80))
        fn = "dynrange.slice_100_from%s,%s,%s.png" % tuple(hkl0)
        plt.savefig(os.path.join(outdir, fn))
    return

def test_plotDynRangeOfSlices2():
    sample = loadSampleYml(sample_yml_path)
    psilist = np.arange(-5, 90., 0.5)
    Ei = 100.
    hkl0s = [[h,0,l] for h in range(-3, 3)
             for l in range(-3,3)]
    hkl_dir = [0., 1., 0]
    xaxis = np.arange(-6, 6, .1)
    for hkl0 in hkl0s:
        plt.figure()
        dynrange.plotDynRangeOfSlice(
            sample, psilist, Ei, hkl0, hkl_dir, xaxis,
            ARCS.scattering_angle_constraints,
            Erange=(-5, 80))
        fn = "dynrange.slice_010_from%s,%s,%s.png" % tuple(hkl0)
        plt.savefig(os.path.join(outdir, fn))
    return

def test_plotDynRangeOfSlices3():
    sample = loadSampleYml(sample_yml_path)
    psilist = np.arange(-5, 90., 0.5)
    Ei = 100.
    hkl0s = [[h,k,0] for k in range(-3, 3)
             for h in range(-3,3)]
    hkl_dir = [0., 0, 1]
    xaxis = np.arange(-6, 6, .1)
    for hkl0 in hkl0s:
        plt.figure()
        dynrange.plotDynRangeOfSlice(
            sample, psilist, Ei, hkl0, hkl_dir, xaxis,
            ARCS.scattering_angle_constraints,
            Erange=(-5, 80))
        fn = "dynrange.slice_001_from%s,%s,%s.png" % tuple(hkl0)
        plt.savefig(os.path.join(outdir, fn))
    return

def main():
    # test_iterPointsInSlice()
    # test_plotDynRangeOfSlice()
    test_plotDynRangeOfSlice2()
    # test_plotDynRangeOfSlices()
    # test_plotDynRangeOfSlices2()
    # test_plotDynRangeOfSlices3()
    return


if __name__ == '__main__': main()

# End of file 
