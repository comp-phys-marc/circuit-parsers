OPENQASM 2.0;
include "qelib1.inc";

sdg q[0];
s q[0];
h q[1];
y q[1];
cx q[0], q[1];