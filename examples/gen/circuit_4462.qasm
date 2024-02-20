OPENQASM 2.0;
include "qelib1.inc";

x q[0];
sdg q[1];
h q[0];
s q[1];
cx q[1], q[0];