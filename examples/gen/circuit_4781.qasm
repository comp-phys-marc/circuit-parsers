OPENQASM 2.0;
include "qelib1.inc";

s q[0];
h q[1];
z q[0];
y q[1];
cx q[1], q[0];