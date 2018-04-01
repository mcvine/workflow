
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
