import pdfquery
import numpy as np
from lxml import etree
from operator import itemgetter
from copy import deepcopy
from dataclasses import dataclass
from qasm_builder import Builder
from typing import Optional


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


@dataclass
class Gate(object):
    name: str
    index: int
    source: Optional[int] = None
    source_index: Optional[int] = None
    ready: Optional[bool] = False
    wire: Optional[str] = None

    def __hash__(self):
        return int.from_bytes(f'{self.name}{self.source}{self.source_index}{self.index}'.encode('utf-8'), 'little')

    def __getitem__(self, item):
        return getattr(self, item)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


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
            skip = False
            for w in wires.keys():
                if np.abs(float(y) - float(w)) < 10:  # merge with wire by proximity
                    skip = True
            if skip:
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
                                        # sort the CNOT position with respect to both wires' gates
                                        gate_params = {'name': 'cx', 'source': source_y, 'index': ctrl}
                                        wires[source_y].append(Gate(**gate_params))
                                        wires[source_y] = sorted(wires[source_y], key=itemgetter('index'))

                                        for source_index, gate in enumerate(wires[source_y]):
                                            if gate['name'] == 'cx' \
                                                    and gate['source'] == source_y \
                                                    and gate['index'] == ctrl:
                                                break

                                        gate_params = {
                                            'name': 'cx',
                                            'source': source_y,
                                            'source_index': source_index,
                                            'index': ctrl
                                        }
                                        wires[wire].append(Gate(**gate_params))
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
                if np.abs(float(wire) - float(w)) < 10:  # merge with wire by proximity
                    wire = w
                    break
            for w in wires.keys():
                if np.abs(float(wire) - float(w)) < 100:  # check if its part of the circuit
                    wires[wire] = []
                    break
        # register the gate
        if text in GATES:
            wires[wire].append({'name': text, 'index': element.attrib['x0'], 'wire': wire})
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
            wires[wire].append({'name': 'custom:' + text, 'index': element.attrib['x0'], 'wire': wire})
            # sort the wire's gates by x index
            wires[wire] = sorted(wires[wire], key=itemgetter('index'))


builder = Builder()

delegated = {}
w = 0


def process_gates(gates, wire, delegating=False):
    to_del = []

    for i, gate in enumerate(gates):
        if not 'custom' in gate['name'] and not 'cx' in gate['name']:
            # This is a gate in the standard library
            getattr(builder, gate['name'])(list(wires.keys()).index(gate['wire']))
        elif 'cx' in gate['name']:
            if gate['source'] == wire and not delegating:
                # delegates all the rest of this wire's gates until after the ctrl-x is printed on the target wire
                gate.ready = True
                gate.wire = wire
                delegated[gate] = gates[i:]
                gates = gates[0:i]
                break
            else:
                # delegates this and following gates until all previous gates from source wire are processed
                found = False
                # we already have gates delegated and waiting on this
                delegates = list(delegated.keys())
                for delegate in delegates:
                    if delegate in delegated.keys():  # otherwise it was removed
                        if delegate['name'] == 'cx' \
                                and delegate['source'] == gate['source']\
                                and delegate['index'] == gate['index']\
                                and delegate['source'] != wire\
                                and delegate['ready'] == True:

                            found = True
                            getattr(builder, gate['name'])(list(wires.keys()).index(gate['source']),
                                                           list(wires.keys()).index(wire))
                            to_del_subs, del_gates = process_gates(delegated[delegate][1:], delegate['wire'])
                            to_del.append(delegate)
                            to_del += to_del_subs
                            delegated[delegate] = del_gates

                            if gate in delegated.keys():
                                to_del_subs, del_gates = process_gates(delegated[gate][1:], gate['wire'])
                                to_del.append(gate)
                                to_del += to_del_subs
                                delegated[gate] = del_gates

                if not found and not delegating:
                    # otherwise we delegate this
                    gate.wire = wire
                    delegated[gate] = gates[i:]  # should include the cnot
                    gates = gates[0:i]
                    break
                if not found and delegating and i == 0:
                    break
        else:
            # This is a custom gate
            name = gate['name'].split(':')[1]
            getattr(builder, 'custom_gate')(name, list(wires.keys()).index(wire))

    return to_del, gates


while len(delegated.keys()) > 0 or w < len(wires.keys()):
    if not w >= len(list(wires.keys())):
        wire = list(wires.keys())[w]
        gates = wires[wire]
        to_del = []

        to_del_plus, gates = process_gates(gates, wire)
        to_del += to_del_plus
        wires[wire] = gates

        for delegate in to_del:
            del delegated[delegate]

        to_del = []

    # try to process delegated gates after each wire is printed
    for k, delegated_gates in delegated.items():
        to_del_plus, delegated_gates_sub = process_gates(delegated_gates, k.wire, delegating=True)
        to_del += to_del_plus
        delegated[k] = delegated_gates_sub

    for delegate in to_del:
        del delegated[delegate]

    w += 1

builder.print()
