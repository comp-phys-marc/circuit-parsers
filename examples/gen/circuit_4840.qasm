OPENQASM 2.0;
include "qelib1.inc";

s q[0];
sdg q[1];
x q[1];
cx q[1], q[0];