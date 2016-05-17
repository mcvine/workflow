# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
utils to create phonon data in IDF format from phonopy data
"""

from . import call_phonopy
from phonopy.interface import vasp

import numpy as np


def make_all(N, supercell_matrix, atom_chemical_symbols, fix_pols_phase=True):
    """ compute all phonon data needed by the single crystal phonon
    kernel.
    
    Inputs
      - N: number of points along each axis
      - supercell_matrix: supercell matrix used in phonpy calculation
      - atom_chemical_symbols: list of atom symbols
      - POSCAR: vasp POSCAR file
    
    Output:
      - Omega2
      - Polarizations
      - Qgridinfo
      - DOS
    
    """
    make_omega2_pols(
        N, supercell_matrix, atom_chemical_symbols, fix_phase=fix_pols_phase)
    make_gridinfo(N, atom_chemical_symbols)
    from .dos import fromOmaga2
    fromOmaga2()
    xtal_xyz = ''.join(atom_chemical_symbols) + '.xyz'
    make_crystal_xyz(xtal_xyz, atom_chemical_symbols)
    return


def make_omega2_pols(N, supercell_matrix, atom_chemical_symbols, fix_phase=True):
    """compute polarizations
    
    Inputs
      - N: number of points along each axis
      - supercell_matrix: supercell matrix used in phonpy calculation
      - POSCAR: vasp POSCAR file
    
    Output:
      - Omega2
      - Polarizations
    """
    print "* Constructing Q array"
    delta = 1./(N-1)
    Qx = np.arange(0, 1.+delta/2, delta)
    Qy = np.arange(0, 1.+delta/2, delta)
    Qz = np.arange(0, 1.+delta/2, delta)
    Qs = []
    for qx in Qx:
        for qy in Qy:
            for qz in Qz:
                Qs.append([qx,qy,qz])
                continue
    Qs =  np.array(Qs)
    
    # !!! only need one symbol per specie
    # !!! follow vasp convention !!!
    atoms = atom_chemical_symbols
    print "* Calling phonopy to compute eigen values and eigen vectors"
    qvecs, freq, pols = call_phonopy.onGrid(atoms, Qs, supercell_matrix, freq2omega=1)
    
    print "* Writing out freqencies"
    from mccomponents.sample.idf import Omega2, Polarizations
    omega2 = freq**2 * 1e24 * (2*np.pi)**2
    Omega2.write(omega2)

    # phase factor for pols
    print "* Fixing and writing out polarizations"
    nq, nbr, natoms, three = pols.shape
    assert three is 3
    if fix_phase:
        atoms = vasp.read_vasp("POSCAR", atom_chemical_symbols)
        positions = atoms.get_scaled_positions()
        for iatom in range(natoms):
            qdotr = np.dot(Qs, positions[iatom]) * 2 * np.pi
            phase = np.exp(1j * qdotr)
            pols[:, :, iatom, :] *= phase[:, np.newaxis, np.newaxis]
            continue
    Polarizations.write(pols)
    return


def make_gridinfo(N, atom_chemical_symbols):
    """Create Q gridinfo file in IDF format

    inputs:
      - N: number of points along each axis
      - vasp POSCAR file in cwd
    """
    from phonopy.interface import vasp
    import numpy as np
    atoms = vasp.read_vasp("POSCAR", atom_chemical_symbols)
    reci_cell = np.linalg.inv(atoms.cell) * 2*np.pi
    # output
    ostream  = open("Qgridinfo", 'wt')
    # reciprocal cell
    for i in range(3):
        ostream.write("b%d = %s\n" % (i+1, list(reci_cell[i])))
        continue
    # grid
    N = [N, N, N]
    for i in range(3):
        ostream.write("n%d = %s\n" % (i+1, N[i]))
        continue
    ostream.close()
    return


def make_crystal_xyz(outpath, atom_chemical_symbols):
    from phonopy.interface import vasp
    atoms = vasp.read_vasp("POSCAR", atom_chemical_symbols)
    # # of atoms
    lines = [str(len(atoms.get_chemical_symbols()))]
    # lattice
    c = atoms.cell.copy()
    c.shape = -1
    lines.append("\t".join(map(str, c)))
    # atoms and positions
    symbols = atoms.get_chemical_symbols()
    positions = atoms.get_scaled_positions()
    for s, p in zip(symbols, positions):
        line = "%s\t%s" % (s, ' '.join(map(str, p)))
        lines.append(line)
        continue
    text = '\n'.join(lines)
    # output stream
    ostream = open(outpath, 'wt')
    ostream.write(text)
    return
    

# End of file 
