OPENQASM 2.0;
include "qelib1.inc";

sdg q[0];
z q[0];
x q[1];
cx q[0], q[1];
y q[1];