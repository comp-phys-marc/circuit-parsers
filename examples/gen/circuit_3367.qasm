OPENQASM 2.0;
include "qelib1.inc";

h q[0];
cx q[1], q[0];
s q[0];
sdg q[1];