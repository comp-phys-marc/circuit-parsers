OPENQASM 2.0;
include "qelib1.inc";

s q[0];
z q[1];
h q[0];
cx q[1], q[0];