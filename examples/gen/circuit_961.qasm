OPENQASM 2.0;
include "qelib1.inc";

cx q[0], q[1];
sdg q[1];
s q[0];
y q[1];