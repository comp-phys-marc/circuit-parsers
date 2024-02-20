OPENQASM 2.0;
include "qelib1.inc";

h q[1];
cx q[0], q[1];
sdg q[0];
z q[1];