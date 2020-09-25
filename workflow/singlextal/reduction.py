# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import numpy as np, os

def slice2hist(ifile, ofile):
    import histogram as H, histogram.hdf as hh
    from mantid import simpleapi as msa

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
    return

def getslice(angles, filenames,
             lattice_params, orientation,
             Eaxis, Qproj_axes,
             output, smooth=True):
    a,b,c,alpha,beta,gamma = lattice_params
    u,v = orientation.u, orientation.v

    from mantid.simpleapi import Load, CompressEvents, DeleteWorkspace, mtd,\
        SetGoniometer, SetUB, CropWorkspace, ConvertToMD, MDNormDirectSC,\
        CloneMDWorkspace, RemoveWorkspaceHistory, SmoothMD, SaveMD
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
        print(dims)
        a2,b2=MDNormDirectSC('md_i_use', **dims)

        #
        print('rotation angle #%s: %s' % (i, angles[i]))

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

    if smooth:
        # smooth data
        DataSmooth2=SmoothMD(InputWorkspace=dataMD2, WidthVector=3, Function='Hat',InputNormalizationWorkspace=normMD2)
        NormSmooth2=SmoothMD(InputWorkspace=normMD2, WidthVector=3, Function='Hat',InputNormalizationWorkspace=normMD2)
        SmoothedSlice=DataSmooth2/NormSmooth2

        SaveMD(InputWorkspace='SmoothedSlice',Filename=output)
    else:
        Slice = dataMD2/normMD2
        SaveMD(InputWorkspace="Slice", Filename=output)
    return


def reduceScan(psi_axis, nxs_template, outfn_template, eiguess, eaxis):
    """run reductions on all given directories
    
    - psi axis: (min,max,delta) for constructing psi angles in degrees
    - nxs_template: template for input nxs path
    - outfn_template: template for output file path
    - eiguess: Ei in meV
    - eaxis: Emin, Emax, dE
    """
    psis = np.arange(*psi_axis)
    for psi in psis:
        nxsfile = nxs_template % tuple([psi]*nxs_template.count("%s"))
        outfile = outfn_template % tuple([psi]*outfn_template.count("%s"))
        reduceOneKeepingEvents(nxsfile, psi, eiguess, eaxis, outfile)
    return


def reduceOneKeepingEvents(nxsfile, angle, eiguess, eaxis, outfile, t0guess=0.):
    """reduce nxs from one angle of a single crystal scan, keeping events
    (only do tof->E conversion)

    nxsfile: input path
    angle: psi in degrees
    eiguess: Ei in meV
    eaxis: Emin, Emax, dE
    outfile: output path
    """
    from mantid.simpleapi import DgsReduction, SofQW3, SaveNexus, SaveNXSPE, LoadInstrument, Load, MoveInstrumentComponent, AddSampleLog
    outfile = os.path.abspath(outfile)
    print("* working on reducing %s to %s" % (nxsfile, outfile))
    # load workspace from input nexus file
    workspace = Load(nxsfile)

    # workspace name have to be unique
    unique_name = os.path.dirname(nxsfile).split('/')[-1]
    wsname = 'reduced-%s' % unique_name

    # Ei
    if eiguess == 0.:
        # If user does not supply Ei, we try to get it from the samplelog,
        # because mcvine-generated SEQUOIA data files are mantid-processed nexus file
        # with sample logs of Ei and t0.
        # If we don't have them from sample logs, we just set Ei and T0 to None
        run = workspace.getRun()
        UseIncidentEnergyGuess = False
        try:
            Ei = run.getLogData('mcvine-Ei').value
            UseIncidentEnergyGuess = True
        except:
            Ei = None
        try:
            T0 = run.getLogData('mcvine-t0').value
        except:
            T0 = None
    else:
        # user specified Ei, just use that
        Ei = eiguess
        T0 = t0guess
        UseIncidentEnergyGuess = True
    # keep events (need to then run RebinToWorkspace and ConvertToDistribution)
    Emin, Emax, dE = eaxis
    eaxis = '%s,%s,%s' % (Emin,dE, Emax)
    DgsReduction(
        SampleInputWorkspace = workspace,
        IncidentEnergyGuess = Ei,
        TimeZeroGuess = T0,
        UseIncidentEnergyGuess=UseIncidentEnergyGuess,
        OutputWorkspace=wsname,
        SofPhiEIsDistribution='0',
        EnergyTransferRange = eaxis,
        )

    AddSampleLog(Workspace=wsname,LogName="psi",LogText=str(angle),LogType="Number")
    SaveNexus(
        InputWorkspace=wsname,
        Filename = outfile,
        Title = 'reduced',
        )
    return

# End of file 
