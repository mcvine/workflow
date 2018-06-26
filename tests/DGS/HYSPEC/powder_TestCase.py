#!/usr/bin/env python

import unittest, os, sys, shutil


class TestCase(unittest.TestCase):
    
    def test(self):
        "mcvine workflow powder --instrument=HYSPEC --detector-vessel-angle 10"
        cmd = "mcvine workflow powder --instrument=HYSPEC --detector-vessel-angle 10 --workdir mcvine-workflow-powder-hyspec"
        if os.system(cmd): raise RuntimeError("%s failed" % cmd)
        wfdir = "mcvine-workflow-powder-hyspec"
        assert os.path.exists(wfdir) and os.path.isdir(wfdir)
        cmd = 'diff %s/Makefile expected-Makefile' % wfdir
        if os.system(cmd): raise RuntimeError("%s failed" % cmd)
        shutil.rmtree(wfdir)
        return


if __name__ == '__main__': unittest.main()
