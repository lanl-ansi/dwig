% This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the ran algorithm  A random number seed of 0 was used.
% chimera_cell_size : 8
% chimera_degree : 12
% generated : 2017-03-03 04:43:18.493065
% generator : ran

set of int: Domain = {-1,1};
float: offset = 0.0;

var Domain: x0;
var Domain: x1;
var Domain: x2;
var Domain: x3;
var Domain: x4;
var Domain: x5;
var Domain: x6;
var Domain: x7;

var float: objective = offset + 1.0*x0 + 1.0*x1 + -1.0*x2 + -1.0*x3 + 1.0*x4 + -1.0*x5 + 1.0*x6 + -1.0*x7 + -1.0*x0*x4 + 1.0*x0*x5 + 1.0*x0*x6 + 1.0*x0*x7 + -1.0*x1*x4 + 1.0*x1*x5 + 1.0*x1*x6 + -1.0*x1*x7 + 1.0*x2*x4 + 1.0*x2*x5 + 1.0*x2*x6 + 1.0*x2*x7 + -1.0*x3*x4 + 1.0*x3*x5 + 1.0*x3*x6 + 1.0*x3*x7;

solve minimize objective;

output [show(objective), " - ", show([x0, x1, x2, x3, x4, x5, x6, x7])];
