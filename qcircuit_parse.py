import pdfquery
from lxml import etree
from operator import itemgetter

from qasm_builder import Builder


GATES = [
    'x',
    'y',
    'z',
    'u1',
    'u2',
    'u3',
    's',
    'sdg',
    'h',
    'tdg',
    'cx',
    'cy',
    'cz',
    't',
    'ccx',
    'reset',
    'cu1',
    'ccy',
    'ccz'
]

pdf = pdfquery.PDFQuery("examples/pdf/Circuits.pdf")
pdf.load()

pdf.tree.write('examples/pdf/readable.xml', pretty_print=True)

tree = etree.parse(open("examples/pdf/readable.xml", "r"))
root = tree.getroot()

wires = {}

for element in root.iter(tag=etree.Element):
    if 'x0' in element.attrib.keys():
        print("%s - %s - (%s, %s)" % (element.tag, element.text, element.attrib['x0'], element.attrib['y0']))

    # if we have a wire
    if element.tag == 'LTTextLineHorizontal':
        # get the vertical position
        y = element.attrib['y0']
        # register the wire
        if y not in wires.keys():
            wires[y] = []

    # if we have a gate
    if element.tag == 'LTTextBoxHorizontal':
        # find the wire
        wire = element.attrib['y0']
        # register the wire if needed
        if wire not in wires.keys():
            wires[wire] = []
        # register the gate
        if element.text.strip().lower() in GATES:
            wires[wire].append({'name': element.text.strip().lower(), 'index': element.attrib['x0']})
            # sort the wire's gates by x index
            wires[wire] = sorted(wires[wire], key=itemgetter('index'))

qasm = ''

builder = Builder()

for wire, gates in wires.items():
    for gate in gates:
        getattr(builder, gate['name'])(list(wires.keys()).index(wire))

print(builder.qasm)
