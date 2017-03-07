% id : 1389262404
% description : This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the fl algorithm.  A random number seed of 0 was used.
% 
% chimera_cell_size : 8
% chimera_degree : 12
% dwig_generator : fl

set of int: Domain = {-1,1};
float: offset = 0.0;
float: scale = 1.0;

var Domain: x0;
var Domain: x1;
var Domain: x2;
var Domain: x4;
var Domain: x5;
var Domain: x6;
var Domain: x8;
var Domain: x9;
var Domain: x10;
var Domain: x11;
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

var float: objective = -0.5*x0*x4 + -0.5*x0*x96 + -0.5*x1*x97 + -0.5*x2*x5 + -0.5*x2*x6 + -0.5*x5*x13 + -0.5*x6*x14 + -0.5*x8*x15 + -0.5*x8*x104 + -1.0*x9*x15 + -1.0*x9*x105 + -0.5*x10*x15 + -0.5*x10*x106 + 0.5*x11*x13 + -0.5*x11*x14 + -0.5*x96*x101 + -0.5*x96*x102 + -0.5*x96*x103 + -0.5*x97*x100 + -1.0*x97*x103 + -0.5*x98*x101 + -1.0*x98*x102 + -0.5*x98*x103 + -0.5*x99*x102 + -0.5*x99*x103 + 0.5*x100*x108 + -1.0*x102*x110 + 0.5*x103*x111 + -0.5*x104*x110 + -1.0*x105*x108 + -0.5*x105*x109 + -0.5*x105*x111 + 0.5*x106*x108 + -0.5*x107*x109 + -0.5*x107*x110;

solve minimize objective;

output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([x0, x1, x2, x4, x5, x6, x8, x9, x10, x11, x13, x14, x15, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111])];
