OPENQASM 2.0;
include "qelib1.inc";

y q[0];
s q[1];
z q[0];
sdg q[1];
cx q[0], q[1];