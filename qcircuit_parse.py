import pdfquery
import numpy as np
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

TOKENS = {
    'control': '•'
}

pdf = pdfquery.PDFQuery("examples/pdf/Circuits.pdf")
pdf.load()

pdf.tree.write('examples/pdf/readable.xml', pretty_print=True)

tree = etree.parse(open("examples/pdf/readable.xml", "r"))
root = tree.getroot()

wires = {}
controls = {}
curve_y_extents = []
curve_x_extents = []

for element in root.iter(tag=etree.Element):
    if 'x0' in element.attrib.keys():
        print("%s - %s - (%s, %s)" % (element.tag, element.text, element.attrib['x0'], element.attrib['y0']))

    # if we have a wire
    if element.tag == 'LTTextLineHorizontal':
        # get the vertical position
        y = element.attrib['y0']
        # register the wire
        if y not in wires.keys():
            if len(wires.keys()) == 0:
                wires[y] = []
                continue
            for w in wires.keys():
                if np.abs(float(y) - float(w)) < 100:  # check if its part of the circuit
                    wires[y] = []
                    break

    # if we have a curve
    if element.tag == 'LTCurve':  # TODO: can we rely on these coming after the controls dict is populated?

        # collect curve extents
        curve_y_extents.append(float(element.attrib['y0']))
        curve_y_extents.append(float(element.attrib['y1']))
        curve_x_extents.append(float(element.attrib['x0']))
        curve_x_extents.append(float(element.attrib['x1']))

        # if we have all the curve extents of a CNOT gate
        if len(curve_y_extents) == 8:
            for wire in wires.keys():
                # find the target wire
                if float(wire) <= max(curve_y_extents):  # TODO: There must be a better criteria
                    for w in controls.keys():
                        ctrls = controls[w]
                        for ctrl in ctrls:
                            # find the controls
                            if min(curve_x_extents) <= float(ctrl) <= max(curve_x_extents):
                                # reverse lookup controls
                                for source_y in controls.keys():
                                    if ctrl in controls[source_y]:
                                        source = source_y
                                        # TODO: find connecting lines
                                        # for el in root.iter(tag=etree.Element):
                                        #     if el.tag == 'LTLine' and el.attrib['x0'] == el.attrib['x1']:
                                        #         if el.attrib['x0'] == ctrl:
                                        #             pass
                                        wires[wire].append({'name': 'cx', 'source': source, 'index': ctrl})
                                        # sort the wire's gates by x index
                                        wires[wire] = sorted(wires[wire], key=itemgetter('index'))
                                        break
                    break
    else:
        curve_y_extents = []
        curve_x_extents = []

    # if we have a gate
    if element.tag == 'LTTextBoxHorizontal':
        # find the wire
        wire = element.attrib['y0']
        # get the text
        text = element.text.strip().lower()
        # register the wire if needed
        if wire not in wires.keys():
            if len(wires.keys()) == 0:
                wires[wire] = []
                continue
            for w in wires.keys():
                if np.abs(float(wire) - float(w)) < 100:  # check if its part of the circuit
                    wires[wire] = []
                    break
        # register the gate
        if text in GATES:
            wires[wire].append({'name': text, 'index': element.attrib['x0']})
            # sort the wire's gates by x index
            wires[wire] = sorted(wires[wire], key=itemgetter('index'))
        # if this is a part of a controlled gate register the control
        elif text in list(TOKENS.values()):
            if text == TOKENS['control']:
                if wire in controls.keys():
                    controls[wire].append(element.attrib['x0'])
                    controls[wire] = sorted(controls[wire])
                else:
                    controls[wire] = [element.attrib['x0']]
        # register custom gates
        elif wire in wires.keys():  # filters out page numbering etc.
            wires[wire].append({'name': 'custom:' + text, 'index': element.attrib['x0']})
            # sort the wire's gates by x index
            wires[wire] = sorted(wires[wire], key=itemgetter('index'))

builder = Builder()

for wire, gates in wires.items():
    for gate in gates:
        if not 'custom' in gate['name'] and not 'cx' in gate['name']:
            # This is a gate in the standard library
            getattr(builder, gate['name'])(list(wires.keys()).index(wire))
        elif 'cx' in gate['name']:
            getattr(builder, gate['name'])(list(wires.keys()).index(gate['source']), list(wires.keys()).index(wire))
        else:
            # This is a custom gate
            name = gate['name'].split(':')[1]
            getattr(builder, 'custom_gate')(name, list(wires.keys()).index(wire))

builder.print()
print(controls)
