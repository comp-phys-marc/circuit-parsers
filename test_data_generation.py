import os
import pathlib

from qcircuit_parse import parse_circuit, Gate, GATES
from circuit_builder import Builder

from pdf2image import convert_from_path

from math import floor
from copy import deepcopy
from itertools import permutations, combinations
from functools import reduce


def convert_pdf_to_image(path_to_pdf="examples/pdf/Circuits.pdf", path_to_image="examples/pdf/Circuits.jpg"):
    """
    Converts a pdf circuit drawing to an image.

    :param path_to_pdf: The path to the pdf to convert.
    :param path_to_image: The path to the output.
    """
    pages = convert_from_path(path_to_pdf, 500)
    for page in pages:
        page.save(path_to_image, 'JPEG')


def generate_pdfs(circuit_depth=2, qubits=2, folder="examples/gen"):
    """
    Generates LaTeX, pdfs and images for the permutations of supported gates on the
    given number of qubits with the provided circuit depth.

    :param circuit_depth: The depth of the circuits to generate.
    :param qubits: The number of qubits in the circuits to generate.
    :param folder: The folder to hold the outputs.
    """
    circuits = []
    # place CNOTs
    positions = [j for j in range(circuit_depth * (qubits - 1))]
    # number of CNOTs
    for length in range(1, circuit_depth * (qubits - 1)):
        # placements of CNOTs
        for combination in combinations(positions, length):
            # orientations of CNOTs
            for permutation in permutations(['up', 'down'], length):
                # init circuit
                circuit = [[Gate(name='I', index=i) for i in range(circuit_depth)] for wire in range(qubits)]
                # add CNOTs to circuit
                for k, source_index in enumerate(combination):
                    # TODO: support CNOTs from non-adjacent wires
                    if permutation[k] == 'up':
                        cnot = Gate(
                            name='cx',
                            source_index=source_index % circuit_depth,
                            source=floor(source_index / circuit_depth),
                            index=source_index % circuit_depth,
                            target=floor(source_index / circuit_depth) + 1
                        )
                    else:
                        cnot = Gate(
                            name='cx',
                            source_index=source_index % circuit_depth,
                            target=floor(source_index / circuit_depth),
                            index=source_index % circuit_depth,
                            source=floor(source_index / circuit_depth) + 1
                        )
                    circuit[cnot['source']][cnot['source_index']] = cnot
                    circuit[cnot['target']][cnot['index']] = cnot

                # permutations of single qubit gates
                single_qubit_gates = len(list(
                    filter(lambda gate: gate['name'] == 'I', reduce(lambda x, y: x + y, circuit))
                ))

                def place_single_qubit_gate(gate, index, circuit):
                    """
                    Places a single qubit gate in the circuit populated with CNOTs.

                    :param gate: The gate to place.
                    :param index: The single gate index to place the gate in.
                    :param circuit: The circuit to place the gate in.

                    :return: The populated circuit.
                    """
                    wire = 0
                    i = 0
                    total = -1
                    prev = (0, 0)
                    while wire < len(circuit) and i < len(circuit[0]) and total < index:
                        prev = (wire, i)
                        if circuit[wire][i]['name'] in list(filter(lambda g: g != 'cx', GATES)):
                            total += 1
                        i += 1
                        if i >= len(circuit[0]):
                            wire += 1
                            i = 0
                    if total >= index:
                        gate.index = prev[1]
                        circuit[prev[0]][prev[1]] = gate

                    return circuit

                gts = list(filter(lambda g: g != 'cx', GATES))
                # rewrite this line so the list isn't built out in its entirety prior to looping
                # but rather is procedurally generated.
                for permutation in permutations(gts, single_qubit_gates):
                    # final circuit lists
                    circuit = deepcopy(circuit)
                    for pg_index, permuted_gate in enumerate(permutation):
                        # add a single qubit gate to the circuit
                        circuit = place_single_qubit_gate(Gate(name=permuted_gate), pg_index, circuit)
                    circuits.append(circuit)

    for num, circuit in enumerate(circuits):
        builder = Builder(pad=False)
        wire = 0
        seen_cxs = []
        i = 0
        while wire < len(circuit) and i < len(circuit[0]):
            gate = circuit[wire][i]
            if 'cx' not in gate['name']:
                getattr(builder, gate['name'])(wire)
            elif gate['source'] == wire:

                # This block only works for depth 2 circuits
                if i == 0 and i not in seen_cxs:
                    builder.cx(gate['source'], gate['target'])
                    seen_cxs.append(i)
                elif i == 1 and i not in seen_cxs:
                    seen_cxs.append(i)
                elif i == 1 and i in seen_cxs:
                    builder.cx(gate['source'], gate['target'])

                builder.tex_cx_source('up' if gate['source'] < gate['target'] else 'down')
            elif gate['target'] == wire:

                # This block only works for depth 2 circuits
                if i == 0 and i not in seen_cxs:
                    builder.cx(gate['source'], gate['target'])
                    seen_cxs.append(i)
                elif i == 1 and i not in seen_cxs:
                    seen_cxs.append(i)
                elif i == 1 and i in seen_cxs:
                    builder.cx(gate['source'], gate['target'])

                builder.tex_cx_target()
            i += 1
            if i >= len(circuit[0]):
                builder.new_tex_wire()
                wire += 1
                i = 0

        builder.print_qasm_file(f"{folder}/circuit_{num}.qasm")
        builder.print_tex_file(f"{folder}/circuit_{num}.tex")
        os.system(f"cd {folder} && pdflatex circuit_{num}.tex")
        if not pathlib.Path(f"{folder}/{num}").is_dir():
            os.mkdir(f"{folder}/{num}")
            convert_pdf_to_image(f"{folder}/circuit_{num}.pdf", f"{folder}/{num}/circuit_{num}.jpg")
        else:
            i = 0
            while os.path.exists(f"{folder}/{num}/circuit_{num + i}.jpg"):
                i += 1
            convert_pdf_to_image(f"{folder}/circuit_{num}.pdf", f"{folder}/{num}/circuit_{num + i}.jpg")


if __name__ == "__main__":
    generate_pdfs()
