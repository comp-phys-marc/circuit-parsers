import random


class Builder:
    """
    A class that represents a quantum circuit.
    """

    def __init__(self, num_qubits=1, qasm="", symbol='q', pad=False):
        """
        Initializes a quantum state with the given parameters.

        :param num_qubits: The total number of qubits.
        :param qasm: Predefined qasm provided to initialization.
        :raises: ValueError
        """
        self.num_qubits = num_qubits
        self.symbol = symbol
        self.pad = pad

        self.header = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'
        self.regs = f'qreg {self.symbol}[{num_qubits}];\ncreg c[{num_qubits}];'
        self.qasm = qasm
        self.custom_gates = ""

        if self.pad:
            self.tex_header = """
\\documentclass{article}
\\usepackage{qcircuit}
\\usepackage{lipsum}  
\\begin{document}""" + self.tex_random_lipsum() + """
\\begin{center}
\\begin{minipage}[c]{1\linewidth}
\\Qcircuit @C=1em @R=.7em {
"""
            self.tex_footer = """}
\\end{minipage}
\\end{center}""" + self.tex_random_lipsum() + """
\\end{document}
        """

        else:
            self.tex_header = """
\\documentclass{article}
\\usepackage{qcircuit}
\\begin{document}
\\Qcircuit @C=1em @R=.7em {
"""
            self.tex_footer = """}
\\end{document}
        """

        self.tex_circuit = ""

    def new_tex_wire(self):
        """
        Increments the wire in the LaTeX circuit.

        :return: self
        """
        self.tex_circuit += ' \\\\ \n'
        return self

    @property
    def tex(self):
        return self.tex_header + self.tex_circuit + self.tex_footer

    @property
    def program(self):
        return self.header + self.custom_gates + self.qasm

    def barrier(self, qubit=None):
        """
        Applies a barrier to the circuit to disable circuit optimization.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        if qubit:
            print("barrier ({0})".format(qubit))
            self.qasm = self.qasm + f'\nbarrier {self.symbol}[{qubit}];'
        else:
            print("barrier ({0})".format(self.symbol))
            self.qasm = self.qasm + f'\nbarrier {self.symbol};'
        return self

    def custom_gate(self, name, qubit, qasm_only=False, tex_only=False):
        """
        Registers a custom gate on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full wasm after the operation.
        """
        print("{1} ({0})".format(qubit, name))
        if not tex_only:
            self.custom_gates += f'gate {name} qargs' + '\n{\n//TODO: replace me!\nU(0,0,0) qargs;\n}\n'
            self.qasm = self.qasm + f'\n{name} {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{{0}}'.format(name)
        return self

    def x(self, qubit, qasm_only=False, tex_only=False):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("x ({0})".format(qubit))
        if not tex_only:
            self.qasm = self.qasm + f'\nx {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{X}'
        return self

    def y(self, qubit, qasm_only=False, tex_only=False):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("y ({0})".format(qubit))
        if not tex_only:
            self.qasm = self.qasm + f'\ny {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{Y}'
        return self

    def z(self, qubit, qasm_only=False, tex_only=False):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("z ({0})".format(qubit))
        if not tex_only:
            self.qasm = self.qasm + f'\nz {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{Z}'
        return self

    def u1(self, lamb, qubit, qasm_only=False, tex_only=False):
        """
        A single parameter single qubit phase gate with zero duration:

        [[1,0],[0,exp(1i*lamb)]]

        :param lamb: The phase parameter.
        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("u1({1}) ({0})".format(qubit, lamb))
        if not tex_only:
            self.qasm = self.qasm + f'\nu1({lamb}) {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{U1({0})}'.format(lamb)
        return self

    def u3(self, theta, phi, lamb, qubit, qasm_only=False, tex_only=False):
        """
        A three parameter single qubit gate:

        [[cos(theta/2),-exp(1i*lambda)*sin(theta/2)],[exp(1i*phi)*sin(theta/2),exp(1i*lambda+1i*phi)*cos(theta/2)]]

        :param theta: The first parameter.
        :param phi: The second parameter.
        :param lamb: The thrid parameter.
        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("u3({1}, {2}, {3}) ({0})".format(qubit, theta, phi, lamb))
        if not tex_only:
            self.qasm = self.qasm + f'\nu3({theta},{phi},{lamb}) {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{U3({0}, {1}, {2})}'.format(theta, phi, lamb)
        return self

    def s(self, qubit, qasm_only=False, tex_only=False):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("s ({0})".format(qubit))
        if not tex_only:
            self.qasm = self.qasm + f'\ns {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{S}'
        return self

    def sdg(self, qubit, qasm_only=False, tex_only=False):
        """
        Performs an S dagger phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("sdg ({0})".format(qubit))
        if not tex_only:
            self.qasm = self.qasm + f'\nsdg {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{S^\\dagger}'
        return self

    def tex_random_lipsum(self):
        """
        Returns a random paragraph of text in LaTeX.
        :return: the command for a random paragraph of text.
        """
        n = random.randint(1, 50)
        return f'\n\\lipsum[{n}-{n}]\n'

    def tex_cx_source(self,  direction):
        """
        Adds a ctrl to the LaTeX circuit with the provided directionality.

        TODO: support CNOTs from non-adjacent wires.

        :param: Whether the target is in the positive (up) or negative (down) direction from the source.
        :return: self
        """
        if direction == 'up':
            self.tex_circuit += ' & \\ctrl{1}'
        else:
            self.tex_circuit += ' & \\ctrl{-1}'
        return self

    def tex_cx_target(self):
        """
        Adds a CNOT target to the circuit.

        :return: self
        """
        self.tex_circuit += ' & \\targ'
        return self

    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param target: The target qubit.
        :return: The full qasm after the operation.
        """
        print("cx ({0} -> {1})".format(source, target))
        self.qasm = self.qasm + f'\ncx {self.symbol}[{source}], {self.symbol}[{target}];'
        return self

    def ccx(self, source_one, source_two, target):
        """
        Performs a multiply controlled X gate on the target qubit with the
        source qubits as controllers.

        :param source_one: The first source qubit.
        :param source_two: The second source qubit.
        :param target: The target qubit.
        :return: The full qasm after the operation.
        """
        print("ccx ({0},{1} -> {2})".format(source_one, source_two, target))
        self.qasm = self.qasm + f'\nccx {self.symbol}[{source_one}], {self.symbol}[{source_two}], {self.symbol}[{target}];'
        return self

    def I(self, qubit, qasm_only=False, tex_only=False):
        """
        Performs an identity on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        if not qasm_only:
            self.tex_circuit += ' & \\qw'
        return self

    def h(self, qubit, qasm_only=False, tex_only=False):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :param qasm_only: Whether to only update the circuit qasm.
        :param tex_only: Whether to only update the circuit LaTeX.
        :return: The full qasm after the operation.
        """
        print("h ({0})".format(qubit))
        if not tex_only:
            self.qasm = self.qasm + f'\nh {self.symbol}[{qubit}];'
        if not qasm_only:
            self.tex_circuit += ' & \\gate{H}'
        return self

    def m(self, qubit):
        """
        Measures the target qubit.

        :param qubit: The target qubit.
        :return: The result of the measurement.
        """
        print("m ({0})".format(qubit))
        self.qasm = self.qasm + f'\nmeasure {self.symbol}[{qubit}] -> c[{qubit}];'
        return self

    def print(self):
        """
        Prints the full qasm.
        """
        print("\nIBMQX QASM:")
        print(self.program)

    def print_qasm_file(self, file_name):
        """
        Prints the QASM to a file.

        :param file_name: The name of the file to print.
        """
        file = open(file_name, 'w+')
        file.write(self.program)
        file.flush()
        file.close()

    def print_tex_file(self, file_name):
        """
        Prints the LaTeX to a file.

        :param file_name: The name of the file to print.
        """
        file = open(file_name, 'w+')
        file.write(self.tex)
        file.flush()
        file.close()
