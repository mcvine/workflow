#!/usr/bin/env python

import unittest, os, sys, shutil


class TestCase(unittest.TestCase):
    
    def test(self):
        "mcvine workflow powder"
        cmd = "mcvine workflow powder --instrument=CNCS"
        if os.system(cmd): raise RuntimeError("%s failed" % cmd)
        wfdir = "mcvine-workflow-powder-CNCS-V"
        assert os.path.exists(wfdir) and os.path.isdir(wfdir)
        cmd = 'cd %s/beam; mcvine instruments cncs beam  --ncount=4e6 --nodes=2' % wfdir
        if os.system(cmd):
            raise RuntimeError("%s failed" % cmd)
        cmd = 'cd %s; make NCOUNT=2e6 NODES=2' % wfdir
        if os.system(cmd):
            raise RuntimeError("%s failed" % cmd)
        shutil.rmtree(wfdir)
        return


if __name__ == '__main__': unittest.main()
