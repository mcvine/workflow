[![Build Status](https://github.com/mcvine/workflow/workflows/CI/badge.svg)](https://github.com/mcvine/workflow/actions?query=workflow%3ACI)
[![Build Status](https://travis-ci.com/mcvine/workflow.svg?branch=master)](https://travis-ci.com/mcvine/workflow) 

# workflow
Scripts and helper files for mcvine workflows

This is intended to be lightweight so that users can easily download this package,
and use the relevant workflow for their work.
This is expected to be updated often.

mcvine/resources is for larger data files and resource files that does not change much
over time, and is most likely installed by a system administrator.


# sample yaml file

A sample can be specified by using a yaml file. Here is an example

```
name: Al-can
structure_file: V.cif
excitation:
 type: powderSQE
 SQEhist: Al-iqe.h5
 Qrange: 0./angstrom, 10./angstrom
 Erange: -45*meV, 45.*meV
shape:
  difference:
    - cylinder:
        radius: 10.*cm
        height: 10*cm
    - cylinder:
        radius: 9.9*cm
        height: 11*cm
temperature: 300*K
```

More examples can be found at [test data directory](tests/data).
