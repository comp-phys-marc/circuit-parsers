OPENQASM 2.0;
include "qelib1.inc";

s q[0];
z q[0];
cx q[0], q[1];
sdg q[1];