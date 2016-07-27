#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>

import mcvine.cli
from mcvine_workflow.singlextal.XtalOrientation import XtalOrientation
from mcvine_workflow.singlextal.scaffolding import spinwave

import numpy as np

def test_spinwave():
    spinwave.createSample(
        outdir='sample', name='sample', xtalori)
    return


def main():
    test_spinwave()
    return


if __name__ == '__main__': main()

# End of file 
