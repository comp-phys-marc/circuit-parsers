OPENQASM 2.0;
include "qelib1.inc";

z q[0];
y q[1];
h q[0];
cx q[1], q[0];