OPENQASM 2.0;
include "qelib1.inc";

s q[0];
y q[0];
x q[1];
cx q[0], q[1];
sdg q[1];