OPENQASM 2.0;
include "qelib1.inc";

h q[0];
s q[1];
cx q[0], q[1];
cx q[1], q[0];