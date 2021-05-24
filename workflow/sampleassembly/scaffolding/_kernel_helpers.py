import os, shutil

def copyfile(fn, srcdir, destdir):
    """copy file to the destdir. This is preferred because we want the sampleassembly
    directory to be complete without and can be copied to anywhere easily.
    This can be done because usually sampleassembly directory should not be too large.
    """
    if not os.path.isabs(fn):
        fn = os.path.join(srcdir, fn)
    assert os.path.exists(fn), "%s does not exist" % fn
    print("Copying {} to {}/".format(fn, destdir))
    basename = os.path.basename(fn)
    outpath = os.path.join(destdir, basename)
    shutil.copyfile(fn, outpath)
    return basename

def copydirectory(dirname, srcdir, destdir):
    """copy a data directory to the destdir.
    This is preferred because we want the sampleassembly
    directory to be complete without and can be copied to anywhere easily.
    This can be done because usually sampleassembly directory should not be too large.
    """
    if not os.path.isabs(dirname):
        dirname = os.path.join(srcdir, dirname)
    assert os.path.exists(dirname), "%s does not exist" % dirname
    print("Copying {} to {}/".format(dirname, destdir))
    basename = os.path.basename(dirname)
    target = os.path.join(destdir, basename)
    shutil.copytree(dirname, target)
    return basename

