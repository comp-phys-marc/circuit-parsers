OPENQASM 2.0;
include "qelib1.inc";

y q[0];
cx q[1], q[0];
s q[0];
z q[1];