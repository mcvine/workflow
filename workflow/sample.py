
def loadSampleYml(path):
    """load sample object from a yaml file
    """
    from mcvine.cli.config import loadYmlConfig
    sample = loadYmlConfig(path)
    # convert input data types
    #  - lattice
    bv = map(eval, sample.lattice.basis_vectors)
    if hasattr(sample.lattice, "primitive_basis_vectors"):
        pbv = map(eval, sample.lattice.primitive_basis_vectors)
    else:
        pbv = None
    sample.lattice.basis_vectors = bv
    sample.lattice.primitive_basis_vectors = pbv
    # - orientation (only for single crystal)
    if not hasattr(sample, 'orientation'):
        sample.orientation = None
    so = sample.orientation
    if so:
        so.u, so.v = map(eval, (so.u, so.v))
    # - excitations. normalize to a list, which could be empty
    excitations = getattr(sample, 'excitations', [])
    excitation = getattr(sample, 'excitation', None)
    if excitation is not None:
        excitations.append(excitation)
    sample.excitations = excitations
    if hasattr(sample, 'excitation'):
        del sample.excitation
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
    values = map(parser.parse, s.split(','))
    u = parser.parse(unit)
    try:
        sum(values, u)
    except:
        raise ValueError("The units for should be %s. Got %s" % (unit, s))
    return tuple(v/u for v in values)
def _to_str_tuple_with_unit(floats, unit):
    return tuple('%s * %s' % (f, unit) for f in floats)
