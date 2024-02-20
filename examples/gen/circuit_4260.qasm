OPENQASM 2.0;
include "qelib1.inc";

sdg q[1];
x q[0];
y q[1];
cx q[0], q[1];