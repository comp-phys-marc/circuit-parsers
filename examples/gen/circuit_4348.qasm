OPENQASM 2.0;
include "qelib1.inc";

x q[1];
h q[0];
y q[1];
cx q[0], q[1];