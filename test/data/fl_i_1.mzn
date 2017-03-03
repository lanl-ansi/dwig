% This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the fl algorithm  A random number seed of 0 was used.
% chimera_cell_size : 8
% chimera_degree : 12
% generated : 2017-03-03 22:24:34.778860
% generator : fl

set of int: Domain = {-1,1};
float: offset = 0.0;

var Domain: x0;
var Domain: x1;
var Domain: x2;
var Domain: x3;
var Domain: x4;
var Domain: x5;
var Domain: x7;
var Domain: x8;
var Domain: x9;
var Domain: x10;
var Domain: x11;
var Domain: x12;
var Domain: x13;
var Domain: x14;
var Domain: x15;
var Domain: x96;
var Domain: x97;
var Domain: x98;
var Domain: x99;
var Domain: x100;
var Domain: x101;
var Domain: x102;
var Domain: x103;
var Domain: x104;
var Domain: x105;
var Domain: x106;
var Domain: x107;
var Domain: x108;
var Domain: x109;
var Domain: x110;
var Domain: x111;

var float: objective = offset + -0.5*x0*x7 + -0.5*x0*x96 + 0.5*x1*x4 + -0.5*x1*x97 + -0.5*x2*x4 + -0.5*x2*x5 + -0.5*x2*x7 + -0.5*x2*x98 + -0.5*x3*x4 + -0.5*x3*x5 + -0.5*x4*x12 + 0.5*x8*x12 + -1.0*x8*x15 + -0.5*x8*x104 + -0.5*x9*x13 + -0.5*x9*x14 + -1.0*x9*x15 + -1.0*x9*x105 + -0.5*x10*x12 + -0.5*x10*x13 + -1.0*x10*x106 + -0.5*x11*x12 + -0.5*x11*x14 + -1.0*x11*x107 + -0.5*x96*x103 + -0.5*x97*x100 + -1.0*x98*x102 + -0.5*x98*x103 + -0.5*x99*x100 + -0.5*x99*x101 + -1.0*x100*x108 + -0.5*x101*x109 + -1.0*x102*x110 + -0.5*x104*x109 + -1.0*x104*x110 + -1.0*x105*x108 + -0.5*x106*x109 + 0.5*x106*x111 + -1.0*x107*x108 + -0.5*x107*x109 + -0.5*x107*x111;

solve minimize objective;

output [show(objective), " - ", show([x0, x1, x2, x3, x4, x5, x7, x8, x9, x10, x11, x12, x13, x14, x15, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111])];
