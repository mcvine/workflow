import sys
nxsfile = sys.argv[1]
angle = sys.argv[2]
eiguess = eval(sys.argv[3])
eaxis = eval(sys.argv[4])
outfile = sys.argv[5]

from mantid.simpleapi import DgsReduction, SofQW3, SaveNexus, SaveNXSPE, LoadInstrument, Load, MoveInstrumentComponent, AddSampleLog

print "* working on ", nxsfile
# load workspace from input nexus file
workspace = Load(nxsfile)
    
# workspace name have to be unique
import os
unique_name = os.path.dirname(nxsfile).split('/')[-1]
wsname = 'reduced-%s' % unique_name

# keep events (need to then run RebinToWorkspace and ConvertToDistribution)
DgsReduction(
    SampleInputWorkspace = workspace,
    IncidentEnergyGuess=eiguess,
    UseIncidentEnergyGuess=True,
    OutputWorkspace=wsname,
    SofPhiEIsDistribution='0',
    EnergyTransferRange = eaxis,
    )

AddSampleLog(Workspace=wsname,LogName="psi",LogText=angle,LogType="Number")

SaveNexus(
    InputWorkspace=wsname,
    Filename = outfile,
    Title = 'reduced',
    )
