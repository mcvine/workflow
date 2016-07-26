# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import numpy as np

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
        nxsfile = nxs_template % (psi,)
        outfile = outfn_template % (psi,)
        reduceOneKeepingEvents(nxsfile, psi, eiguess, eaxis, outfile)
    return


def reduceOneKeepingEvents(nxsfile, angle, eiguess, eaxis, outfile):
    """reduce nxs from one angle of a single crystal scan, keeping events
    (only do tof->E conversion)

    nxsfile: input path
    angle: psi in degrees
    eiguess: Ei in meV
    eaxis: Emin, Emax, dE
    outfile: output path
    """
    from mantid.simpleapi import DgsReduction, SofQW3, SaveNexus, SaveNXSPE, LoadInstrument, Load, MoveInstrumentComponent, AddSampleLog

    print "* working on ", nxsfile
    # load workspace from input nexus file
    workspace = Load(nxsfile)

    # workspace name have to be unique
    import os
    unique_name = os.path.dirname(nxsfile).split('/')[-1]
    wsname = 'reduced-%s' % unique_name

    # keep events (need to then run RebinToWorkspace and ConvertToDistribution)
    Emin, Emax, dE = eaxis
    eaxis = '%s,%s,%s' % (Emin,dE, Emax)
    DgsReduction(
        SampleInputWorkspace = workspace,
        IncidentEnergyGuess=eiguess,
        UseIncidentEnergyGuess=False,
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
