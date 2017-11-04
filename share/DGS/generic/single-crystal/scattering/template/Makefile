# -*- Makefile -*-
# single crystal scan workflow: one angle
#

# *** modifye the following if running mannualy ***
# *** or use command line to change them.       ***
INSTRUMENT=%(instrument)s
# NCOUNT=1e7
# BUFFER_SIZE=1000000
# NODES=10

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
event-nxs: sim_$(SAMPLE_ANGLE).nxs

# nexus file comes from collecting scattered neutrons at the detector system
sim_$(SAMPLE_ANGLE).nxs: out/scattered-neutrons
	INSTRUMENT=$(INSTRUMENT) NODES=$(NODES) SAMPLE_ANGLE=$(SAMPLE_ANGLE) time ./create-nxs >log.create-nxs 2>&1

# scattered neutrons comes from simulation of scattering of incident beam by sample assembly
out/scattered-neutrons: beam sampleassembly
	NCOUNT=$(NCOUNT) BUFFER_SIZE=$(BUFFER_SIZE) NODES=$(NODES) SAMPLE_ANGLE=$(SAMPLE_ANGLE) ./scatter </dev/null >log.scatter 2>&1

scattering: out/scattered-neutrons

beam:
	ln -s ../../beam

sampleassembly:
	ln -s ../../sampleassembly
