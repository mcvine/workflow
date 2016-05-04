#!/usr/bin/env python

import unittest, os, sys, shutil


class TestCase(unittest.TestCase):
    
    def test(self):
        "mcvine workflow phonon.from_phonopy"
        from mcvine.resources import sample
        src = sample(name='Si', temperature='100K', shape='dummy')
        src = os.path.join(os.path.dirname(src), 'phonons', 'vasp-phonopy')
        shutil.copytree(src, 'work')
        from mcvine_workflow.phonon.from_phonopy import make_all
        os.chdir('work')
        make_all(N=50, supercell_matrix=(5,5,5), atom_chemical_symbols=['Si'])
        return


if __name__ == '__main__': unittest.main()
