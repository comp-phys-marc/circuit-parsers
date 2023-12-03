OPENQASM 2.0;
include "qelib1.inc";

sdg q[0];
x q[0];
cx q[1], q[0];
z q[1];