class Builder:
    """
    A class that represents a quantum circuit.
    """

    def __init__(self, num_qubits=1, qasm=None, symbol='Q'):
        """
        Initializes a quantum state with the given parameters.

        :param num_qubits: The total number of qubits.
        :param qasm: Predefined qasm provided to initialization.
        :raises: ValueError
        """
        self.num_qubits = num_qubits
        self.symbol = symbol

        if qasm is None:
            self.qasm = f'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg {self.symbol}[{num_qubits}];\ncreg c[{num_qubits}];'
        else:
            self.qasm = qasm

        self.print()

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

    def x(self, qubit):
        """
        Performs a Pauli X gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("x ({0})".format(qubit))
        self.qasm = self.qasm + f'\nx {self.symbol}[{qubit}];'
        return self

    def y(self, qubit):
        """
        Performs a Pauli Y gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("y ({0})".format(qubit))
        self.qasm = self.qasm + f'\ny {self.symbol}[{qubit}];'
        return self

    def z(self, qubit):
        """
        Performs a Pauli Z gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("z ({0})".format(qubit))
        self.qasm = self.qasm + f'\nz {self.symbol}[{qubit}];'
        return self

    def u1(self, lamb, qubit):
        """
        A single parameter single qubit phase gate with zero duration:

        [[1,0],[0,exp(1i*lamb)]]

        :param lamb: The phase parameter.
        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("u1({1}) ({0})".format(qubit, lamb))
        self.qasm = self.qasm + f'\nu1({lamb}) {self.symbol}[{qubit}];'
        return self

    def u3(self, theta, phi, lamb, qubit):
        """
        A three parameter single qubit gate:

        [[cos(theta/2),-exp(1i*lambda)*sin(theta/2)],[exp(1i*phi)*sin(theta/2),exp(1i*lambda+1i*phi)*cos(theta/2)]]

        :param theta: The first parameter.
        :param phi: The second parameter.
        :param lamb: The thrid parameter.
        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("u3({1}, {2}, {3}) ({0})".format(qubit, theta, phi, lamb))
        self.qasm = self.qasm + f'\nu3({theta},{phi},{lamb}) {self.symbol}[{qubit}];'
        return self

    def s(self, qubit):
        """
        Performs an S phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("s ({0})".format(qubit))
        self.qasm = self.qasm + f'\ns {self.symbol}[{qubit}];'
        return self

    def sdg(self, qubit):
        """
        Performs an S dagger phase shift gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("sdg ({0})".format(qubit))
        self.qasm = self.qasm + f'\nsdg {self.symbol}[{qubit}];'
        return self

    def cx(self, source, target):
        """
        Performs a Controlled X gate on the target qubit with the
        source qubit as controller.

        :param source: The source qubit.
        :param source: The target qubit.
        :return: The full qasm after the opeation.
        """
        print("cx ({0} -> {1})".format(source, target))
        self.qasm = self.qasm + f'\ncx {self.symbol}[{source}], {self.symbol}[{target}];'
        return self

    def h(self, qubit):
        """
        Performs a Hadamard gate on the target qubit.

        :param qubit: The target qubit.
        :return: The full qasm after the operation.
        """
        print("h ({0})".format(qubit))
        self.qasm = self.qasm + f'\nh {self.symbol}[{qubit}];'
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
        print(self.qasm)
