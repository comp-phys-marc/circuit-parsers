OPENQASM 2.0;
include "qelib1.inc";

x q[0];
h q[1];
y q[0];
cx q[1], q[0];