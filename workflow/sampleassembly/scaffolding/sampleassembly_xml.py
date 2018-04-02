import numpy as np, os
from mcni.units import parser
parser = parser()

def create(scatterers):
    text = [templates.header]
    geometer_registrations = []
    Ts = []
    for scatterer in scatterers:
        # get scatterer data
        scatterer_dict = scatterer.__dict__.copy()
        # format shape
        scatterer_dict['shape'] = _format_shape(scatterer_dict['shape'])
        #
        text.append( templates.scatterer % scatterer_dict )
        geometer_registrations.append( templates.geometer_register % scatterer_dict )
        Ts.append(parser.parse(scatterer.temperature))
        continue
    import warnings
    warnings.warn("assume average temperature")
    T = np.sum(Ts)/len(Ts)
    text.append(templates.geometer % dict(registrations=''.join(geometer_registrations)))
    text.append(templates.environment % dict(temperature=T))
    text.append(templates.footer)
    return '\n'.join(text)


def _format_shape(shape):
    indent = 6 * ' '
    # shape is an xml string
    if shape.startswith('<'):
        return '\n'.join( indent + x for x in shape.splitlines() )
    # shape is a simple oneliner that can convert to a xml tag
    if '\n' not in shape:
        return '%s<%s />' % (indent, shape)
    # yml shape specification
    raise NotImplementedError


class templates:
    header = """<?xml version="1.0"?>

<!DOCTYPE SampleAssembly>

<SampleAssembly name="X"
   max_multiplescattering_loops_among_scatterers="1"
   max_multiplescattering_loops_interactM_path1="4"
   min_neutron_probability=".1"
 >
"""

    scatterer = """
  <PowderSample name="%(name)s" type="sample">
    <Shape>
%(shape)s
    </Shape>
    <Phase type="crystal">
      <ChemicalFormula>%(chemical_formula)s</ChemicalFormula>
      <xyzfile>%(name)s.xyz</xyzfile>
    </Phase>
  </PowderSample>
"""

    geometer = """
  <LocalGeometer registry-coordinate-system="InstrumentScientist">
%(registrations)s
  </LocalGeometer>
"""

    geometer_register = """
    <Register name="%(name)s" position="(0,0,0)" orientation="(0, 0, 0)"/>
"""

    environment = """
  <Environment temperature="%(temperature)s"/>
"""

    footer = """
</SampleAssembly>
"""
