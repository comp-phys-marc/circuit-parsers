OPENQASM 2.0;
include "qelib1.inc";

cx q[1], q[0];
x q[0];
cx q[0], q[1];
s q[1];