OPENQASM 2.0;
include "qelib1.inc";

sdg q[0];
y q[0];
cx q[0], q[1];
z q[1];