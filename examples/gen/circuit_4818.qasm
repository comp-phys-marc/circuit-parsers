OPENQASM 2.0;
include "qelib1.inc";

s q[0];
h q[0];
z q[1];
sdg q[1];
cx q[1], q[0];