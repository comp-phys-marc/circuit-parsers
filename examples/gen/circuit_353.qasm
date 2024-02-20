OPENQASM 2.0;
include "qelib1.inc";

cx q[0], q[1];
y q[0];
z q[1];
sdg q[0];
s q[1];