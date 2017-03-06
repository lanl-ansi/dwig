% This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the fl algorithm  A random number seed of 0 was used.
% chimera_cell_size : 8
% chimera_degree : 12
% generated : 2017-03-06 22:09:20.149736
% generator : fl

set of int: Domain = {-1,1};
float: offset = 0.0;

var Domain: x0;
var Domain: x2;
var Domain: x3;
var Domain: x4;
var Domain: x5;
var Domain: x6;
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

var float: objective = offset + -0.25*x0*x4 + -0.5*x0*x5 + -0.5*x0*x6 + -0.25*x0*x7 + -0.5*x0*x96 + -0.25*x2*x4 + -0.25*x2*x5 + -0.5*x2*x98 + -0.25*x3*x4 + -0.5*x3*x6 + 0.25*x3*x7 + -0.5*x3*x99 + -0.25*x4*x12 + -0.25*x5*x13 + -0.5*x6*x14 + -0.5*x7*x15 + -0.25*x8*x12 + -0.75*x8*x15 + -0.5*x8*x104 + -0.25*x9*x12 + -0.5*x9*x13 + -0.75*x9*x15 + -1.0*x9*x105 + -0.25*x10*x12 + -0.25*x10*x14 + -0.5*x10*x106 + -0.5*x11*x12 + -0.75*x11*x13 + -0.25*x11*x14 + -1.0*x11*x107 + -0.25*x96*x100 + -0.5*x96*x103 + -0.25*x97*x100 + 0.25*x97*x101 + -0.25*x97*x102 + -0.75*x97*x103 + -0.5*x98*x102 + -0.25*x98*x103 + -0.5*x99*x100 + -0.25*x99*x101 + -0.25*x99*x102 + -0.5*x99*x103 + -0.5*x100*x108 + -0.25*x102*x110 + -0.25*x103*x111 + 0.25*x104*x108 + -0.25*x104*x109 + -0.5*x104*x110 + -0.5*x104*x111 + 0.25*x105*x108 + -0.25*x105*x109 + -0.25*x105*x110 + -0.25*x106*x108 + -0.25*x106*x110 + -0.5*x106*x111 + -0.5*x107*x108 + -0.75*x107*x110 + -0.25*x107*x111;

solve minimize objective;

output [show(objective), " - ", show([x0, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111])];
