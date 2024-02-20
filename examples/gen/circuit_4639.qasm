OPENQASM 2.0;
include "qelib1.inc";

z q[0];
sdg q[1];
y q[0];
cx q[1], q[0];