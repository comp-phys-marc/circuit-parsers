OPENQASM 2.0;
include "qelib1.inc";

sdg q[1];
cx q[0], q[1];
h q[0];
s q[1];