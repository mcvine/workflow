#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal import dynrange
from mcvine_workflow.sample import loadSampleYml

import numpy as np, os

thisdir = os.path.dirname(__file__)
sample_yml_path = os.path.join(thisdir, "..", "..", 'DGS', 'ARCS', 'Si.yml')

def test_iterPointsInSlice():
    sample = loadSampleYml(sample_yml_path)
    psilist = np.arange(-5, 90., 0.5)
    Ei = 100.
    hkl0 = [-16/3., -8/3., 8/3.]
    hkl_dir = [-1., 1., -1.]
    xaxis = np.arange(-6, 6, .1)
    from matplotlib import pyplot as plt
    for psi, xs, Es in dynrange.iterPointsInSlice(
            sample, psilist, Ei, hkl0, hkl_dir, xaxis):
        plt.plot(xs, Es, label=str(psi))
        continue
    plt.show()
    return


def main():
    test_iterPointsInSlice()
    return


if __name__ == '__main__': main()

# End of file 
