#!/usr/bin/env python

import unittest, os, sys, shutil, subprocess as sp

class TestCase(unittest.TestCase):
    
    def test_kernelorientation(self):
        "mcvine workflow sxu kernelorientation"
        cmd = "mcvine workflow sxu kernelorientation KVO.yml"
        o = sp.check_output(cmd.split())
        self.assertEqual(o.strip(), "0.0,1.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0")
        return

    def test_solve_psi(self):
        "mcvine workflow sxu solve_psi"
        cmd = "mcvine workflow sxu solve_psi Si.yml --Ei=100 --hkl -5.33333 -2.66667 2.66667 --E 40 --psimin -5. --psimax 90."
        o = sp.check_output(cmd.split())
        self.assertAlmostEqual(float(o), 46.37473, places=4)
        return

if __name__ == '__main__': unittest.main()
