import os

def rsync(src, dest):
    cmd = 'rsync -aL %s/ %s/' % (os.path.abspath(src), os.path.abspath(dest))
    if os.system(cmd):
        raise RuntimeError("%s failed" % cmd)
    return
