import os


def loadSampleYml(path):
    """load sample object from a yaml file
    """
    from mcvine.cli.config import loadYmlConfig
    sample = loadYmlConfig(path)
    # - crystal structure
    # if the filepath for the atomic structure is given, we should use it
    # to compute everything we can
    if hasattr(sample, 'structure_file'):
        if not os.path.isabs(sample.structure_file):
            parent = os.path.dirname(path)
            sample.structure_file = os.path.join(parent, sample.structure_file)
        _loadStructure(sample.structure_file, sample)
    else:
        # convert input data types
        #  - lattice
        bv = list(map(eval, sample.lattice.basis_vectors))
        if hasattr(sample.lattice, "primitive_basis_vectors"):
            pbv = list(map(eval, sample.lattice.primitive_basis_vectors))
        else:
            pbv = None
        sample.lattice.basis_vectors = bv
        sample.lattice.primitive_basis_vectors = pbv
    # - orientation (only for single crystal)
    if not hasattr(sample, 'orientation'):
        sample.orientation = None
    so = sample.orientation
    if so:
        so.u, so.v = list(map(eval, (so.u, so.v)))
    # - excitations. normalize to a list, which could be empty
    excitations = getattr(sample, 'excitations', [])
    excitation = getattr(sample, 'excitation', None)
    if excitation is not None:
        excitations.append(excitation)
    sample.excitations = excitations
    if hasattr(sample, 'excitation'):
        del sample.excitation
    return sample


def _loadStructure(path, sample):
    "load crystal structure from path and save info in `sample`"
    ext = os.path.splitext(path)[-1][1:]
    from diffpy.Structure.Parsers import getParser
    p = getParser(ext)
    sample.atomic_structure = structure = p.parseFile(path)
    assert not hasattr(sample, 'chemical_formula')
    assert not hasattr(sample, 'lattice')
    atoms = [atom.element for atom in structure]
    from collections import Counter
    atoms_counter = Counter(atoms)
    sample.chemical_formula = ''.join('%s%s' % (a, n) for a,n in atoms_counter.items())
    class Lattice: pass
    lattice = sample.lattice = Lattice()
    sl = structure.lattice
    lattice.constants = sl.a, sl.b, sl.c, sl.alpha, sl.beta, sl.gamma
    lattice.basis_vectors = sl.base
    return sample

    
def dgs_setEi(sample, Ei):
    """set incident energy for DGS experiment
    
A sample has kernels with parameters that may be affected by Ei.
For example, a powder SQE kernel has Qrange and Erange. 
When this sample is put into a beam in a DGS instrument,
it is better to simulate only within the dynamical range determined
by Ei and instrument geometry.
Here we do some quick calculation to estimate the dynamical range
for the given Ei, without considering the instrument geometry.
The main purpose of this is to limit the simulation dynamical
range to speed up the simulation

    Ei: float. unit: meV
    """
    from mcni.utils import conversion
    ki = conversion.e2k(Ei) # \AA^-1
    Qrange = (0., 2*ki)
    Erange = (-Ei, Ei*.99)
    for excitation in sample.excitations:
        if 'Qrange' in excitation.__dict__:
            excitation.Qrange = ','.join(_to_str_tuple_with_unit(
                _combine_range(Qrange, _to_float_tuple(excitation.Qrange, '1./angstrom')),
                '1./angstrom'))
        if 'Erange' in excitation.__dict__:
            excitation.Erange = ','.join(_to_str_tuple_with_unit(
                _combine_range(Erange, _to_float_tuple(excitation.Erange, 'meV')),
                'meV'))
        continue
    return


def _combine_range(r1, r2):
    min1, max1 = r1
    min2, max2 = r2
    return max(min1, min2), min(max1, max2)

from mcni.units import parser
parser = parser()
def _to_float_tuple(s, unit):
    values = list(map(parser.parse, s.split(',')))
    u = parser.parse(unit)
    try:
        sum(values, u)
    except:
        raise ValueError("The units for should be %s. Got %s" % (unit, s))
    return tuple(v/u for v in values)
def _to_str_tuple_with_unit(floats, unit):
    return tuple('%s * %s' % (f, unit) for f in floats)
