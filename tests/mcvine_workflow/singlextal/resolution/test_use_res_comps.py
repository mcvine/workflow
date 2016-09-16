#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal.resolution import use_res_comps

import numpy as np

def test_setup():
    sampleyml = "Si.yml"
    beam = "/SNS/users/lj7/simulations/ARCS/beam/100meV-n1e10"
    E = 40.
    hkl = [-16/3.,-8/3.,8/3.]
    psi_axis = -5, 90., 0.5
    class instrument:
        name = 'ARCS'
        detsys_radius = 3.
    class pixel:
        radius = 0.0254
    use_res_comps.setup(sampleyml, beam, E, hkl, psi_axis, instrument, pixel)
    return


def main():
    test_setup()
    return


if __name__ == '__main__': main()

# End of file 
