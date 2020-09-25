#!/bin/bash

set -e
set -x
conda config --set always_yes true
conda update conda
conda config --add channels conda-forge
conda config --add channels diffpy
conda config --add channels mantid
conda config --add channels mcvine

conda create -n testenv -c mcvine/label/unstable mcvine.instruments=0.1.1 mpich python=$TRAVIS_PYTHON_VERSION # muparser=2.2.5=0 numpy=1.14
source activate testenv

export SRC=$PWD
export PYVER=${TRAVIS_PYTHON_VERSION}
export PREFIX=${CONDA_PREFIX}
echo $PYVER
echo $PREFIX
PY_INCLUDE_DIR=${PREFIX}/include/`ls ${PREFIX}/include/|grep python${PYVER}`
PY_SHAREDLIB=${PREFIX}/lib/`ls ${PREFIX}/lib/|grep libpython${PYVER}[a-z]*.so$`
echo $PY_INCLUDE_DIR
echo $PY_SHAREDLIB
export BLD_ROOT=$SRC/build
mkdir -p $BLD_ROOT && cd $BLD_ROOT
cmake $SRC -DCMAKE_INSTALL_PREFIX=$PREFIX -DPYTHON_LIBRARY=$PY_SHAREDLIB -DPYTHON_INCLUDE_DIR=$PY_INCLUDE_DIR
make install
