OPENQASM 2.0;
include "qelib1.inc";

z q[0];
y q[1];
sdg q[0];
cx q[0], q[1];