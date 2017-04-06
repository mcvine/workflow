# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

class instrument:
    def __init__(self, name, detsys_radius, L_m2s, offset_sample2beam, L_m2fc=None):
        self.name = name
        self.detsys_radius = detsys_radius
        self.L_m2s = L_m2s
        self.offset_sample2beam = offset_sample2beam
        self.L_m2fc = L_m2fc

class pixel:
    def __init__(self, radius, height, pressure, position=None):
        self.radius = radius
        self.height = height
        self.pressure = pressure
        self.position = position

# End of file 
