OPENQASM 2.0;
include "qelib1.inc";

cx q[1], q[0];
h q[0];
sdg q[0];
z q[1];
s q[1];