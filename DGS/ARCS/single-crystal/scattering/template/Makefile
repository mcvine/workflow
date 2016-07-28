# -*- Makefile -*-
# single crystal scan workflow: one angle
#

# this will be overide
SAMPLE_ANGLE=0

all: event-nxs

# clean up
clean:
	rm -rf out work-* log.* *~ *.nxs *.h5

# this rule restore this directory back to the original state of template
# don't do this unless you know what you are doing
restore-template: clean
	rm -f beam
	rm -rf sampleassembly
	rm -rf *.nxs *.h5

# 
event-nxs: sim-$(SAMPLE_ANGLE).nxs

# add meta data
sim-$(SAMPLE_ANGLE).nxs: sim.nxs
	cp sim.nxs sim-$(SAMPLE_ANGLE).nxs
	mcvine instruments $(INSTRUMENT) nxs populate_metadata --type=Ei --beam_outdir=beam/out --nxs=sim-$(SAMPLE_ANGLE).nxs

# nexus file comes from collecting scattered neutrons at the detector system
sim.nxs: out/scattered-neutrons
	time ./create-nxs >log.create-nxs 2>&1

# scattered neutrons comes from simulation of scattering of incident beam by sample assembly
out/scattered-neutrons: beam sampleassembly
	SAMPLE_ANGLE=$(SAMPLE_ANGLE) time ./scatter >log.scatter 2>&1

scattering: out/scattered-neutrons

beam:
	ln -s ../../beam

sampleassembly:
	ln -s ../../sampleassembly
