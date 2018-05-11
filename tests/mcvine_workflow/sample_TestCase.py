#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow import sample
from mcni.utils import conversion as C

import numpy as np, os
here = os.path.dirname(__file__)


def test():
    class powdersqe:
        type = "powderSQE"
        SQEhist = "Al-iqe.h5"
        Erange = "-50*meV,50*meV"
        Qrange = "1/angstrom, 10/angstrom"

    class mysample:
        class lattice:
            constants = 1., 1., 1., 90., 90., 90.
            basis_vectors = [[1,0,0],[0,1,0],[0,0,1]]
        chemical_formula="V"
        class shape:
            class sphere:
                radius = 3
    mysample.excitations = [powdersqe]
    Ei = 30.; ki = C.e2k(Ei)
    sample.dgs_setEi(mysample, Ei)
    Qmin, Qmax = sample._to_float_tuple(mysample.excitations[0].Qrange, '1./angstrom')
    assert np.isclose(Qmin, 1.)
    assert np.isclose(Qmax, 2*ki)
    Emin, Emax = sample._to_float_tuple(mysample.excitations[0].Erange, 'meV')
    assert np.isclose(Emin, -Ei)
    assert np.isclose(Emax, Ei*.99)
    return

def test2():
    sample.loadSampleYml(os.path.join(here, 'data', 'KVO.yml'))
    return


def test3():
    V_plate = sample.loadSampleYml(os.path.join(here, 'data', 'V-plate.yml'))
    assert V_plate.chemical_formula == 'V2'
    assert np.allclose(V_plate.lattice.basis_vectors, np.eye(3)*3.024)
    for atom in V_plate.atomic_structure:
        print atom
    return


def main():
    test()
    test2()
    test3()
    return


if __name__ == '__main__': main()

# End of file 
