# -*- Makefile -*-

# *** modifye the following if running mannualy ***
# *** or use command line to change them.       ***
INSTRUMENT=%(instrument)s
NCOUNT=%(ncount)s
BUFFER_SIZE=%(buffer_size)s
NODES=%(nodes)s
QAXIS=%(qaxis)s
MULSCATT=%(multiple_scattering)s
DETECTOR_VESSEL_ANGLE=%(detector_vessel_angle)s

# default rule: we want I(Q,E)
all: IQE

# clean up
clean:
	rm -rf out work-* log.* *~ *.h5 *.nxs

clean-intermediate-files:
	rm -rf out/rank*-step* work-*/todetsys/out/rank*-step*

# this rule restore this directory back to the original state of template
# don't do this unless you know what you are doing
restore-template: clean
	rm -f beam
	rm -rf sampleassembly
	rm -rf *.nxs *.h5


plot-iqe: IQE
	plothist --min=0 iqe.h5

# IQE comes from iqe histogram file
IQE: iqe.h5

# iqe histogram comes from reduction of simulated event mode nexus file
iqe.h5: sim.nxs
	INSTRUMENT=$(INSTRUMENT) QAXIS="$(QAXIS)" ./reduce2iqe >log.reduce 2>&1

# nexus file comes from collecting scattered neutrons at the detector system
sim.nxs: out/scattered-neutrons
	DETECTOR_VESSEL_ANGLE=$(DETECTOR_VESSEL_ANGLE) INSTRUMENT=$(INSTRUMENT) NODES=$(NODES) ./create-nxs </dev/null >log.create-nxs 2>&1

# scattered neutrons comes from simulation of scattering of incident beam by sample assembly
out/scattered-neutrons: beam sampleassembly sampleassembly/*
	NCOUNT=$(NCOUNT) BUFFER_SIZE=$(BUFFER_SIZE) NODES=$(NODES) MULSCATT=$(MULSCATT) ./scatter </dev/null >log.scatter 2>&1

# Required inputs
beam:
	@echo "** Missing incident beam"
	@echo "** Please create a symbolic link to the incident beam"
	@echo "** For example: ln -s ~/simulations/ARCS/beam/688meV beam"
	exit 1

sampleassembly:
	@echo "** Missing sample assembly"
	@echo "** Please create a sampleassembly directory."
	@echo "** You can do this by copying, for example: cp -a ~/simulations/ARCS/He4/sim/template/sampleassembly ."
	exit 1

