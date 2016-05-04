#!/usr/bin/env python

import histogram as H, histogram.hdf as hh
from mantid import simpleapi as msa

import sys
ifile, ofile = sys.argv[1:]

def eliminateUnitDimension(shape):
    for d in shape:
        if d>1: yield d
    return

ws = msa.Load(ifile)
I = ws.getSignalArray()
I.shape = tuple(eliminateUnitDimension(I.shape))
E2 = ws.getErrorSquaredArray()
E2.shape = I.shape
axes = []
for i in range(ws.getNumDims()):
    dim = ws.getDimension(i)
    if dim.getNBins() > 1:
        axis = H.axis(
            dim.getName(), 
            unit="1",
            centers = [dim.getX(ind) for ind in range(dim.getNBins())]
            )
        axes.append(axis)
    continue
h = H.histogram("slice", axes, data=I, errors=E2)
hh.dump(h, ofile)
