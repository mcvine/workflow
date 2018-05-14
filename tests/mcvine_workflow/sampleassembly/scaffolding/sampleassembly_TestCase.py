#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine.workflow.sample import loadSampleYml
from mcvine.workflow.sampleassembly.scaffolding import createSampleAssembly

import numpy as np, os
here = os.path.dirname(__file__)


def test():
    sample = loadSampleYml(os.path.join(here, 'KVO.yml'))
    createSampleAssembly("_tmp.sampleassembly", sample)
    o = os.system('diff -r _tmp.sampleassembly ' + os.path.join(here, 'expected-sampleassembly'))
    assert not o
    return


def test2():
    sample = loadSampleYml(os.path.join(here, 'KVO-rotated.yml'))
    createSampleAssembly("_tmp.sampleassembly2", sample)
    o = os.system('diff -r _tmp.sampleassembly2 ' + os.path.join(here, 'expected-sampleassembly2'))
    assert not o
    return


def test3():
    sample = loadSampleYml(os.path.join(here, 'KVO-rotated.yml'))
    al_can = loadSampleYml(os.path.join(here, 'al-can.yml'))
    createSampleAssembly("_tmp.sampleassembly3", sample, al_can)
    o = os.system('diff -r _tmp.sampleassembly3 ' + os.path.join(here, 'expected-sampleassembly3'))
    assert not o
    return


def test4():
    sample = loadSampleYml(os.path.join(here, '..', '..', '..', 'data', 'V-plate.yml'))
    createSampleAssembly("_tmp.sampleassembly4", sample)
    o = os.system('diff -r _tmp.sampleassembly4 ' + os.path.join(here, 'expected-sampleassembly4'))
    assert not o
    return


def main():
    test()
    test2()
    test3()
    test4()
    return


if __name__ == '__main__': main()

# End of file 
