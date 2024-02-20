OPENQASM 2.0;
include "qelib1.inc";

sdg q[1];
cx q[1], q[0];
y q[0];
s q[1];