OPENQASM 2.0;
include "qelib1.inc";

cx q[1], q[0];
h q[0];
y q[1];
sdg q[0];
x q[1];