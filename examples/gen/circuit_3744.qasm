OPENQASM 2.0;
include "qelib1.inc";

y q[0];
h q[0];
x q[1];
cx q[0], q[1];