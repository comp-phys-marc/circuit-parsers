OPENQASM 2.0;
include "qelib1.inc";

h q[0];
x q[1];
s q[0];
cx q[1], q[0];