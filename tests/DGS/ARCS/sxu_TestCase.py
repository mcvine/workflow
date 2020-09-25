#!/usr/bin/env python

import unittest, os, sys, shutil, subprocess as sp

class TestCase(unittest.TestCase):
    
    def test_kernelorientation(self):
        "mcvine workflow sxu kernelorientation"
        cmd = "mcvine workflow sxu kernelorientation KVO.yml"
        o = sp.check_output(cmd.split()).strip()
        if sys.version_info >= (3,0) and isinstance(o, bytes):
            o = o.decode()
        self.assertEqual(o, "0.0,1.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0")
        return

    def test_solve_psi(self):
        "mcvine workflow sxu solve_psi"
        cmd = "mcvine workflow sxu solve_psi Si.yml --Ei=100 --hkl -5.33333 -2.66667 2.66667 --E 40 --psimin -5. --psimax 90."
        o = sp.check_output(cmd.split())
        self.assertAlmostEqual(float(o), 46.37473, places=4)
        return

    def test_dr_slice(self):
        "mcvine workflow sxu dr_slice"
        out = "_tmp.slice100_from000.png"
        cmd = "mcvine workflow sxu dr_slice Si.yml --Ei=100 --psi-axis -5 90. 1. --hkl0 0 0 0 --hkl-dir 1 0 0 --x-axis -15 5 .1 --instrument ARCS --Erange -15 80 --out %s" % out
        o = sp.check_output(cmd.split())
        self.assertTrue(os.path.exists(out))
        return


if __name__ == '__main__': unittest.main()
