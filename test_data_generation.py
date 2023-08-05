from qcircuit_parse import parse_circuit, Gate, GATES
from qasm_builder import Builder

from pdf2image import convert_from_path

from copy import deepcopy
from itertools import permutations, combinations


def convert_pdf_to_image(path_to_pdf="examples/pdf/Circuits.pdf", path_to_image="examples/pdf/Circuits.jpg"):
    """
    Converts a pdf circuit drawing to an image.

    :param path_to_pdf: The path to the pdf to convert.
    :param path_to_image: The path to the output.
    """
    pages = convert_from_path(path_to_pdf, 500)
    for page in pages:
        page.save(path_to_image, 'JPEG')


def generate_pdfs(circuit_depth=5, qubits=3):
    """
    Generates LaTeX, pdfs and images for the permutations of supported gates on the
    given number of qubits with the provided circuit depth.

    :param circuit_depth: The depth of the circuits to generate.
    :param qubits: The number of qubits in the circuits to generate.
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
                single_qubit_gates = len(filter(lambda gate: gate['name'] == 'I', reduce(lambda x, y: x + y, circuit)))

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
                    total = 0
                    prev = (0, 0)
                    while wire < len(circuit) and i < len(circuit[0]) and total < index:
                        prev = (wire, i)
                        if circuit[wire][i]['name'] == 'I':
                            total += 1
                        i += 1
                        if i >= len(circuit[0]):
                            wire += 1
                            i = 0
                    if total >= index:
                        gate['index'] = prev[1]
                        circuit[prev[0]][prev[1]] = gate

                    return circuit

                for permutation in permutations(filter(lambda g: g != 'cx', GATES), single_qubit_gates):
                    # final circuit lists
                    circuit = deepcopy(circuit)
                    for pg_index, permuted_gate in enumerate(permutation):
                        # add a single qubit gate to the circuit
                        circuit = place_single_qubit_gate(Gate(name=permuted_gate), pg_index, circuit)
                    circuits.append(circuit)
