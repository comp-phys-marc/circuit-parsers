OPENQASM 2.0;
include "qelib1.inc";

h q[0];
sdg q[0];
y q[1];
s q[1];
cx q[0], q[1];