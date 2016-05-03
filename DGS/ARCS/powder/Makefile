# -*- Makefile -*-

# default rule: we want I(Q,E)
all: IQE

# clean up
clean:
	rm -rf out work-* log.* *~ *.h5 *.nxs

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
iqe.h5: arcs-sim-wEidata.nxs
	./reduce2iqe >log.reduce 2>&1

# Ei data need to be added to the simulated nexus file
arcs-sim-wEidata.nxs: arcs-sim.nxs
	cp arcs-sim.nxs arcs-sim-wEidata.nxs &&\
	mcvine instruments arcs nxs populate_metadata --type=Ei --nxs=arcs-sim-wEidata.nxs --beam_outdir=beam/out

# nexus file comes from collecting scattered neutrons at the detector system
arcs-sim.nxs: out/scattered-neutrons
	./create-nxs </dev/null >log.create-nxs 2>&1

# scattered neutrons comes from simulation of scattering of incident beam by sample assembly
out/scattered-neutrons: beam sampleassembly sampleassembly/*
	./scatter </dev/null >log.scatter 2>&1

# Required inputs
beam:
	@echo "** Missing incident beam"
	@echo "** Please create a symbolic link to the incident beam"
	@echo "** For example: ln -s ~/simulations/ARCS/mod2sample/688meV beam"
	exit 1

sampleassembly:
	@echo "** Missing sample assembly"
	@echo "** Please create a sampleassembly directory."
	@echo "** You can do this by copying, for example: cp -a ~/simulations/ARCS/He4/sim/template/sampleassembly ."
	exit 1

