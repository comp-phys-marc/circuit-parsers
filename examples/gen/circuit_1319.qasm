OPENQASM 2.0;
include "qelib1.inc";

cx q[1], q[0];
z q[0];
s q[1];
sdg q[0];