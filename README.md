# circuit-parsers

A repository for our work on parsing quantum circuit diagrams.

Our data looks like combinations of images (circuits) and text (OpenQASM code). There are
four utilities for working with these provided in this repo. The first is `qcircuit_parse.py`. If 
you already have a circuit as a .pdf and want to know the OpenQASM that goes along with it, you
can provide the path to the .pdf to `qcircuit_parse.parse_circuit` and it will return the QASM as 
a string to you.

The second tool is `test_data_generation.py`. You can call `test_data_generation.generate_pdfs` with
a circuit depth and number of qubits and it will generate the LaTeX files to go with every permutation
of the quantum gates in the supported list (see `qcircuit_parse.GATES`) arranged into a circuit with 
these parameters and with nearest-neighbour connectivity. Then, you can run pdflatex to turn these into
.pdfs. Finally, the utility will generate images (.jpgs) from the .pdfs that result.

The third tool is `image_classification.py` which accepts the image dataset in the examples
folder as an input and runs a basic image classification algorithm on it. Our goal is to improve this
algorithm!

Finally, there is a trained model that will get your circuit classification right about 80% of the time
under saved_models. You can use this model to convert provided circuits to QASM like so:

```
$ python tool.py --input_file path/to/circuit.jpg
```

This will spit out the (hopefully) correct QASM right in the command line.

```
Opening the provided image... 

Classifying the quantum circuit... 
 
Converting to QASM: 
 
OPENQASM 2.0;
include "qelib1.inc";

h q[0];
x q[1];
cx q[0], q[1];
```