OPENQASM 2.0;
include "qelib1.inc";

y q[0];
h q[1];
sdg q[0];
cx q[0], q[1];