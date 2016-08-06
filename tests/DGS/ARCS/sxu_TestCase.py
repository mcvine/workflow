#!/usr/bin/env python

import unittest, os, sys, shutil, subprocess as sp

class TestCase(unittest.TestCase):
    
    def test_kernelorientation(self):
        "mcvine workflow sxu kernelorientation"
        cmd = "mcvine workflow sxu kernelorientation KVO.yml"
        o = sp.check_output(cmd.split())
        self.assertEqual(o.strip(), "0.0,1.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0")
        return

    def test_mkxoyml(self):
        "mcvine workflow sxu mkxoyml"
        cmd = "mcvine workflow sxu mkxoyml KVO.yml KVO-xtalori.yml"
        o = sp.check_output(cmd.split())
        return

if __name__ == '__main__': unittest.main()
