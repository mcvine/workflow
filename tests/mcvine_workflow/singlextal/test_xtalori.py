#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal.xtalori import xtalori2mat, Eresidual
from mcvine_workflow.singlextal.XtalOrientation import XtalOrientation
from mcvine_workflow import singlextal

import numpy as np

def test_xtalori2mat():
    # cubic
    ra, rb, rc = np.array([[1,0,0], [0,1,0], [0,0,1]])
    u,v = np.array([[1,0,0], [0,1,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        (ra,rb,rc))
    
    psi = np.pi/2
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        (-rb, ra, rc))

    # box
    ra, rb, rc = np.array([[1,0,0], [0,2,0], [0,0,3]])
    u,v = np.array([[1,0,0], [0,0.5,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        ([1,0,0],[0,0.5,0],[0,0,1./3]))
    
    u,v = np.array([[0,0,1], [0,1,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        ([0,0,1./3],[0,0.5,0],[-1,0,0]))
    
    # 
    ra, rb, rc = np.array([[1,0,0], [0,1,0], [1,1,1]])
    u,v = np.array([[1,0,0], [0,1,0]])
    psi = 0
    np.testing.assert_array_almost_equal(
        xtalori2mat(ra,rb,rc, u,v, psi),
        ([1,0,0],[0,1,0],[-1,-1,1]))
    
    return


def test_Eresidual():    
    Ei = 100
    Etarget = 35
    angles = np.arange(-5, 89.6, 0.5) # psi angles
    angles = np.arange(40, 49.5, 0.5) # psi angles

    from mcvine.cli.config import loadYmlConfig
    import os
    xtalori = loadYmlConfig("Si-xtalori.yaml")
    l = xtalori.lattice
    for i in range(1,4):
        key = 'a%d' %i
        setattr(l, key, eval(getattr(l, key)))
        continue
    v = np.dot(l.a1, np.cross(l.a2, l.a3))
    b1 = 2*np.pi*np.cross(l.a2, l.a3)/v
    b2 = 2*np.pi*np.cross(l.a3, l.a1)/v
    b3 = 2*np.pi*np.cross(l.a1, l.a2)/v
    xo = xtalori.orientation
    for key in ['u','v']:
        setattr(xo, key, eval(getattr(xo, key)))
        continue
    xtalori = XtalOrientation(b1,b2,b3, xo.u, xo.v, xo.psi)
    # hkl. center of silicon 111 plot
    ex = np.array((1,0,0))
    ey = np.array((0,1,0))
    ez = np.array((0,0,1))
    u = np.array((1, 0.5, -0.5))
    v = np.array((0, -1, -1))
    hkl = -(5+1./3) * u + 0 * v
    
    print "psi\tresidual"
    print Eresidual(xtalori, hkl, Etarget, angles, Ei)
    return


def test_Eresidual2():    
    Ei = 100
    Etarget = 35
    angles = np.arange(-5, 89.6, 0.5) # psi angles
    angles = np.arange(40, 49.5, 0.5) # psi angles

    import os
    xtalori = singlextal.loadXtalOriConfig("Si-xtalori.yaml")
    # hkl. center of silicon 111 plot
    ex = np.array((1,0,0))
    ey = np.array((0,1,0))
    ez = np.array((0,0,1))
    u = np.array((1, 0.5, -0.5))
    v = np.array((0, -1, -1))
    hkl = -(5+1./3) * u + 0 * v
    
    print "psi\tresidual"
    print Eresidual(xtalori, hkl, Etarget, angles, Ei)
    return


def test():
    test_xtalori2mat()
    test_Eresidual()
    test_Eresidual2()
    return


def main():
    test()
    return


if __name__ == '__main__': main()

# End of file 
