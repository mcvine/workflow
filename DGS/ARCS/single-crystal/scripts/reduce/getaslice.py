#!/usr/bin/env python

import numpy as np

def run(angles, filenames, lattice_params, orientation, Eaxis, Qproj_axes, output):
    a,b,c,alpha,beta,gamma = lattice_params
    u,v = orientation.u, orientation.v

    from mantid.simpleapi import Load, CompressEvents, DeleteWorkspace, mtd,\
        SetGoniometer, SetUB, CropWorkspace, ConvertToMD, MDNormDirectSC,\
        CloneMDWorkspace, RemoveWorkspaceHistory, SmoothMD, SaveMD \
        
    WG= Load(','.join(filenames))

    # compress events
    CompressEvents(InputWorkspace=WG,OutputWorkspace='WG_compressed',Tolerance=0.05)
    # clean up
    DeleteWorkspace(WG)
    # obtain the compressed ws
    WG_compressed=mtd['WG_compressed']
    WGO = WG_compressed

    # geometry
    # goniometer psi: rotate around vertical axis. counter-clock wise (ccw)
    SetGoniometer(WGO, Axis0='psi,0,1,0,1')
    # UB: ws, a, b, c, alpha, beta, gamma, u, v
    # SetUB(WGO,7.255,5.002,5.548,90,96.75,90,u=[-0.333333,0,0.333333],v=[0,2,0])
    # SetUB(WGO,a, a, a, 90, 90, 90, u=[-1.,1.,-1.],v=[2., 1., -1.])
    SetUB(WGO,a, b, c, alpha, beta, gamma, u=u,v=v)
    # align the energy axis?
    CropWorkspace(
        InputWorkspace=WGO,OutputWorkspace='WGO_cropped',
        XMin=Eaxis.min,XMax=Eaxis.max)
    WGO_cropped=mtd['WGO_cropped']
    # clean up
    DeleteWorkspace(WGO)


    # min, max values of hklE
    U,V,W = Qproj_axes.U,Qproj_axes.V,Qproj_axes.W
    minn="%s,%s,%s,%s" % (U.min,V.min,W.min,Eaxis.min)
    maxx="%s,%s,%s,%s" % (U.max,V.max,W.max,Eaxis.max)

    for i in range(WGO_cropped.getNumberOfEntries()):
        # convert events to Q vector
        ConvertToMD(
            InputWorkspace=WGO_cropped[i],
            OutputWorkspace='md_i_use',
            dEAnalysisMode="Direct",
            QDimensions='Q3D',
            Q3DFrames="HKL",
            QConversionScales='HKL',
            MinValues=minn,
            MaxValues=maxx,
            Uproj=U.proj,
            Vproj=V.proj,
            Wproj=W.proj)

        # compute data and normalization for the slices at the requested axes
        dims = dict(
            # AlignedDim0='[-H,H,-H],-6.0,6.0, 481',
            AlignedDim0 = '[%s],%s,%s,%s' % (U.proj_name, U.min, U.max, U.N),
            AlignedDim1='DeltaE,%s,%s, %s' % (Eaxis.min, Eaxis.max, Eaxis.N),
            # ,-5.45,-5.15,1',
            AlignedDim2='[%s],%s,%s,%s' % (V.proj_name, V.min, V.max, V.N),
            AlignedDim3='[%s],%s,%s,%s' % (W.proj_name, W.min, W.max, W.N),
            )
        print dims
        a2,b2=MDNormDirectSC('md_i_use', **dims)

        #
        print 'rotation angle #%s: %s' % (i, angles[i])

        # merge data
        if i==0:
            dataMD2=CloneMDWorkspace(a2)
            normMD2=CloneMDWorkspace(b2)
        else:
            dataMD2+=a2
            normMD2+=b2
        continue

    # clean up
    RemoveWorkspaceHistory(dataMD2); RemoveWorkspaceHistory(normMD2)

    # smooth data
    DataSmooth2=SmoothMD(InputWorkspace=dataMD2, WidthVector=3, Function='Hat',InputNormalizationWorkspace=normMD2)
    NormSmooth2=SmoothMD(InputWorkspace=normMD2, WidthVector=3, Function='Hat',InputNormalizationWorkspace=normMD2)
    SmoothedSlice=DataSmooth2/NormSmooth2

    SaveMD(InputWorkspace='SmoothedSlice',Filename=output)
    return


def main():
    import sys
    from config import loadYmlConfig
    config = loadYmlConfig(sys.argv[1])
    angles = np.arange(*eval(config.angles))
    filenames = [config.filename_pattern % dict(angle=angle)
                 for angle in angles]
    print angles[0], filenames[0]
    lattice_params = eval(config.lattice)
    orientation = config.orientation
    Eaxis = config.Eaxis
    Qproj_axes = config.Q_projections
    output = config.output
    run(angles, filenames, lattice_params, orientation, Eaxis, Qproj_axes, output)    
    return


if __name__ == '__main__': main()
