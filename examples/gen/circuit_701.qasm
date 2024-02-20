OPENQASM 2.0;
include "qelib1.inc";

cx q[0], q[1];
sdg q[0];
h q[1];
z q[0];
y q[1];