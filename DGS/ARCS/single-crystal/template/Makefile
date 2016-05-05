# -*- Makefile -*-
# single crystal scan workflow: one angle
#

# this will be overide
SAMPLE_ANGLE=0

all: sim-$(SAMPLE_ANGLE).nxs

# clean up
clean:
	rm -rf out work-* log.* *~ *.nxs *.h5

# this rule restore this directory back to the original state of template
# don't do this unless you know what you are doing
restore-template: clean
	rm -f beam
	rm -rf sampleassembly
	rm -rf *.nxs *.h5

# add meta data
sim-$(SAMPLE_ANGLE).nxs: sim.nxs
	cp sim.nxs sim-$(SAMPLE_ANGLE).nxs
	mcvine instruments $(INSTRUMENT) nxs populate_metadata --type=Ei --beam_outdir=beam/out --nxs=sim-$(SAMPLE_ANGLE).nxs

# nexus file comes from collecting scattered neutrons at the detector system
sim.nxs: out/scattered-neutrons
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
