# -*- Makefile -*-
# ARCS workflow
#

SAMPLE_ANGLE=0

# default rule: we want I(Q,E)
all: IQE

# clean up
clean:
	rm -rf out work-* log.* *~ *.nxs *.h5

# this rule restore this directory back to the original state of template
# don't do this unless you know what you are doing
restore-template: clean
	rm -f beam
	rm -rf sampleassembly
	rm -rf *.nxs *.h5

# # IQE comes from iqe histogram file
IQE: iqe.h5

# reduce
sim.nxspe: arcs-sim-wEiData.nxs
	SAMPLE_ANGLE=$(SAMPLE_ANGLE) time ./reduce2iqe &> log.reduce

# Ei data need to be added to the simulated nexus file
arcs-sim-wEiData.nxs: arcs-sim.nxs
	cp arcs-sim.nxs arcs-sim-wEidata.nxs
	mcvine instruments arcs nxs populate_metadata --type=Ei --beam_outdir=beam/out --nxs=arcs-sim-wEidata.nxs
# 	arcs-nxs-populate-Eidata --nxs=arcs-sim-wEidata.nxs --mod2sample=beam/out

# nexus file comes from collecting scattered neutrons at the detector system
arcs-sim.nxs: out/scattered-neutrons
	time ./create-nxs &> log.create-nxs

# scattered neutrons comes from simulation of scattering of incident beam by sample assembly
out/scattered-neutrons: beam sampleassembly sampleassembly/*
	SAMPLE_ANGLE=$(SAMPLE_ANGLE) time ./scatter &> log.scatter

scattering: out/scattered-neutrons

beam:
	@echo "** Missing incident beam"
	@echo "** Please a symbolic link to the incident beam"
	@echo "** For example: ln -s /SNS/users/linjiao/simulations/ARCS/mod2sample/70meV beam"
	exit 1

sampleassembly:
	@echo "** Missing sample assembly"
	@echo "** Please create sampleassembly directory."
	@echo "** You can do this by copying, for example: cp -a /SNS/users/linjiao/simulations/ARCS/He4/sim/template/sampleassembly ."
	exit 1
