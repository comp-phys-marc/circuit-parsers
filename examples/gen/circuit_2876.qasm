OPENQASM 2.0;
include "qelib1.inc";

y q[0];
sdg q[0];
s q[1];
cx q[1], q[0];
x q[1];