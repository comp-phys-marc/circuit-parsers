OPENQASM 2.0;
include "qelib1.inc";

z q[0];
s q[0];
sdg q[1];
y q[1];
cx q[0], q[1];