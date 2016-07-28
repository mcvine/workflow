#!/usr/bin/env python

import unittest, os, sys, shutil


class TestCase(unittest.TestCase):
    
    def test(self):
        "mcvine workflow singlecrystal"
        cmd = "mcvine workflow singlecrystal --outdir=_tmp.KVO --type=DGS --instrument=ARCS --sample=KVO.yml"
        if os.system(cmd): raise RuntimeError("%s failed" % cmd)
        wfdir = "_tmp.KVO"
        assert os.path.exists(wfdir) and os.path.isdir(wfdir)
        shutil.rmtree(wfdir)
        return


if __name__ == '__main__': unittest.main()
