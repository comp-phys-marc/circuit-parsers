OPENQASM 2.0;
include "qelib1.inc";

z q[0];
x q[0];
sdg q[1];
cx q[1], q[0];
h q[1];