OPENQASM 2.0;
include "qelib1.inc";

z q[0];
s q[0];
h q[1];
x q[1];
cx q[1], q[0];