#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.sample import loadSampleYml
from mcvine.workflow.singlextal.scaffolding import createSampleAssembly

import numpy as np, os
here = os.path.dirname(__file__)


def test():
    sample = loadSampleYml('KVO.yml')
    createSampleAssembly("_tmp.sampleassembly", sample)
    o = os.system('diff -r _tmp.sampleassembly %s/expected-sampleassembly' % here)
    assert not o
    return


def main():
    test()
    return


if __name__ == '__main__': main()

# End of file 
