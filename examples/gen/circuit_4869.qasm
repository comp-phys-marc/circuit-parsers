OPENQASM 2.0;
include "qelib1.inc";

sdg q[0];
y q[0];
x q[1];
s q[1];
cx q[1], q[0];