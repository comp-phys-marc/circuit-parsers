OPENQASM 2.0;
include "qelib1.inc";

h q[0];
sdg q[1];
cx q[0], q[1];
x q[0];
z q[1];