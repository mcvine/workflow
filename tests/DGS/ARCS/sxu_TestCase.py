#!/usr/bin/env python

import unittest, os, sys, shutil, subprocess as sp

class TestCase(unittest.TestCase):
    
    def test(self):
        "mcvine workflow sxu"
        cmd = "mcvine workflow sxu kernelorientation KVO.yml"
        o = sp.check_output(cmd.split())
        self.assertEqual(o.strip(), "0.0,1.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0")
        return

if __name__ == '__main__': unittest.main()
