OPENQASM 2.0;
include "qelib1.inc";

s q[0];
y q[1];
sdg q[0];
cx q[1], q[0];