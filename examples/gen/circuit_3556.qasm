OPENQASM 2.0;
include "qelib1.inc";

x q[0];
sdg q[1];
z q[0];
y q[1];
cx q[0], q[1];