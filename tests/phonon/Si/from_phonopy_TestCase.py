#!/usr/bin/env python

skip = True # this test needs phonopy

import unittest, os, sys, shutil, numpy as np


class TestCase(unittest.TestCase):
    
    def test(self):
        "mcvine workflow phonon.from_phonopy"
        work = '_tmp'
        if os.path.exists(work):
            shutil.rmtree(work)
        from mcvine import deployment_info
        from mcvine.resources import sample
        src = sample(name='Si', temperature='100K', shape='dummy')
        src = os.path.join(os.path.dirname(src), 'phonons', 'vasp-phonopy')
        shutil.copytree(src, work)
        from mcvine_workflow.phonon.from_phonopy import make_all
        os.chdir(work)
        make_all(
            N=10, 
            supercell_matrix=np.eye(3)*5, 
            atom_chemical_symbols=['Si']
        )
        return


if __name__ == '__main__': unittest.main()
