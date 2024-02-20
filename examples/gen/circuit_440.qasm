OPENQASM 2.0;
include "qelib1.inc";

cx q[0], q[1];
z q[0];
h q[1];
y q[0];
x q[1];