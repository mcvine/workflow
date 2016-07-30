#!/usr/bin/env python

import unittest, os, sys, shutil


class TestCase(unittest.TestCase):
    
    def test_spinwave(self):
        "mcvine workflow singlecrystal: spinwave"
        cmd = "mcvine workflow singlecrystal --outdir=_tmp.KVO --type=DGS --instrument=ARCS --sample=KVO.yml"
        if os.system(cmd): raise RuntimeError("%s failed" % cmd)
        wfdir = "_tmp.KVO"
        assert os.path.exists(wfdir) and os.path.isdir(wfdir)
        shutil.rmtree(wfdir)
        return


    def test_phonon(self):
        "mcvine workflow singlecrystal: phonon"
        cmd = "mcvine workflow singlecrystal --outdir=_tmp.Si --type=DGS --instrument=ARCS --sample=Si.yml"
        if os.system(cmd): raise RuntimeError("%s failed" % cmd)
        wfdir = "_tmp.Si"
        assert os.path.exists(wfdir) and os.path.isdir(wfdir)
        shutil.rmtree(wfdir)
        return


if __name__ == '__main__': unittest.main()
