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
        # structure file
        scatterer_dict['structure'] = _format_structure(scatterer)
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
    text = '\n'.join(text)
    return text


def _format_structure(scatterer):
    if getattr(scatterer, 'structure_file', None):
        # if structure_file is already specified,
        # create the tag using the filename
        # the file will be copied by code in ./sample.py
        fn = os.path.basename(scatterer.structure_file)
        _, ext = os.path.splitext(fn)
        tag = '%sfile' % ext[1:]
        return "<%s>%s</%s>" % (tag, fn, tag)
    # otherwise, use xyzfile
    return templates.scatterer_structure_xyz % dict(name=scatterer.name)


def _format_shape(shape):
    from mcni._2to3 import isstr
    if isstr(shape):
        return _format_shape_from_shapexml(shape)
    # shape is a dict
    from instrument.geometry.yaml.parser import Parser
    parser = Parser()
    shape = parser.parse(shape.orig_dict)
    from instrument.geometry.pml import render
    text = render(shape, print_docs=False)
    text = '\n'.join(text)
    lines = text.splitlines()
    # ignore header and footer
    lines = lines[15:-9]
    return '\n'.join(lines)

def _format_shape_from_shapexml(shape):
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
      %(structure)s
    </Phase>
  </PowderSample>
"""

    scatterer_structure_xyz = "<xyzfile>%(name)s.xyz</xyzfile>"
    
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
