% id : 1813382118
% description : This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the clq algorithm.  A random number seed of 0 was used.
% 
% chimera_cell_size : 8
% chimera_degree : 12
% dwig_generator : clq

set of int: Domain = {-1,1};
float: offset = -9.6;

var Domain: x0;
var Domain: x1;
var Domain: x2;
var Domain: x3;
var Domain: x4;
var Domain: x5;
var Domain: x6;
var Domain: x7;

var float: objective = offset + -2.0*x0 + -2.0*x1 + -2.0*x2 + -2.0*x3 + -2.0*x4 + -2.0*x5 + -2.0*x6 + -2.0*x7 + -0.4*x0*x4 + -0.4*x0*x5 + -0.4*x0*x6 + -0.4*x0*x7 + -0.4*x1*x4 + -0.4*x1*x5 + -0.4*x1*x6 + -0.4*x1*x7 + -0.4*x2*x4 + -0.4*x2*x5 + -0.4*x2*x6 + -0.4*x2*x7 + -0.4*x3*x4 + -0.4*x3*x5 + -0.4*x3*x6 + -0.4*x3*x7;

solve minimize objective;

output [show(objective), " - ", show([x0, x1, x2, x3, x4, x5, x6, x7])];
