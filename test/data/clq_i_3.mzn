% id : 1813382118
% description : This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the clq algorithm.  A random number seed of 0 was used.
% 
% chimera_cell_size : 8
% chimera_degree : 12
% dwig_generator : clq

set of int: Domain = {-1,1};
float: offset = 48.0;
float: scale = 1.25;

var Domain: x0;
var Domain: x1;
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
var Domain: x16;
var Domain: x17;
var Domain: x18;
var Domain: x19;
var Domain: x20;
var Domain: x21;
var Domain: x22;
var Domain: x23;
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
var Domain: x112;
var Domain: x113;
var Domain: x114;
var Domain: x115;
var Domain: x116;
var Domain: x117;
var Domain: x118;
var Domain: x119;
var Domain: x192;
var Domain: x193;
var Domain: x194;
var Domain: x195;
var Domain: x196;
var Domain: x197;
var Domain: x198;
var Domain: x199;
var Domain: x200;
var Domain: x201;
var Domain: x202;
var Domain: x203;
var Domain: x204;
var Domain: x205;
var Domain: x206;
var Domain: x207;
var Domain: x208;
var Domain: x209;
var Domain: x210;
var Domain: x211;
var Domain: x212;
var Domain: x213;
var Domain: x214;
var Domain: x215;

var float: objective = 1.6*x0 + 1.6*x1 + 1.6*x2 + 1.6*x3 + 1.6*x4 + 1.6*x5 + 1.6*x6 + 1.6*x7 + 1.6*x8 + 1.6*x9 + 1.6*x10 + 1.6*x11 + 2.0*x12 + 2.0*x13 + 2.0*x14 + 2.0*x15 + 1.6*x16 + 1.6*x17 + 1.6*x18 + 1.6*x19 + 1.6*x20 + 1.6*x21 + 1.6*x22 + 1.6*x23 + 2.0*x96 + 2.0*x97 + 2.0*x98 + 2.0*x99 + 1.6*x100 + 1.6*x101 + 1.6*x102 + 1.6*x103 + 2.0*x104 + 2.0*x105 + 2.0*x106 + 2.0*x107 + 2.0*x108 + 2.0*x109 + 2.0*x110 + 2.0*x111 + 2.0*x112 + 2.0*x113 + 2.0*x114 + 2.0*x115 + 1.6*x116 + 1.6*x117 + 1.6*x118 + 1.6*x119 + 1.6*x192 + 1.6*x193 + 1.6*x194 + 1.6*x195 + 1.6*x196 + 1.6*x197 + 1.6*x198 + 1.6*x199 + 1.6*x200 + 1.6*x201 + 1.6*x202 + 1.6*x203 + 2.0*x204 + 2.0*x205 + 2.0*x206 + 2.0*x207 + 1.6*x208 + 1.6*x209 + 1.6*x210 + 1.6*x211 + 1.6*x212 + 1.6*x213 + 1.6*x214 + 1.6*x215 + 0.4*x0*x4 + 0.4*x0*x5 + 0.4*x0*x6 + 0.4*x0*x7 + 0.4*x0*x96 + 0.4*x1*x4 + 0.4*x1*x5 + 0.4*x1*x6 + 0.4*x1*x7 + 0.4*x1*x97 + 0.4*x2*x4 + 0.4*x2*x5 + 0.4*x2*x6 + 0.4*x2*x7 + 0.4*x2*x98 + 0.4*x3*x4 + 0.4*x3*x5 + 0.4*x3*x6 + 0.4*x3*x7 + 0.4*x3*x99 + 0.4*x4*x12 + 0.4*x5*x13 + 0.4*x6*x14 + 0.4*x7*x15 + 0.4*x8*x12 + 0.4*x8*x13 + 0.4*x8*x14 + 0.4*x8*x15 + 0.4*x8*x104 + 0.4*x9*x12 + 0.4*x9*x13 + 0.4*x9*x14 + 0.4*x9*x15 + 0.4*x9*x105 + 0.4*x10*x12 + 0.4*x10*x13 + 0.4*x10*x14 + 0.4*x10*x15 + 0.4*x10*x106 + 0.4*x11*x12 + 0.4*x11*x13 + 0.4*x11*x14 + 0.4*x11*x15 + 0.4*x11*x107 + 0.4*x12*x20 + 0.4*x13*x21 + 0.4*x14*x22 + 0.4*x15*x23 + 0.4*x16*x20 + 0.4*x16*x21 + 0.4*x16*x22 + 0.4*x16*x23 + 0.4*x16*x112 + 0.4*x17*x20 + 0.4*x17*x21 + 0.4*x17*x22 + 0.4*x17*x23 + 0.4*x17*x113 + 0.4*x18*x20 + 0.4*x18*x21 + 0.4*x18*x22 + 0.4*x18*x23 + 0.4*x18*x114 + 0.4*x19*x20 + 0.4*x19*x21 + 0.4*x19*x22 + 0.4*x19*x23 + 0.4*x19*x115 + 0.4*x96*x100 + 0.4*x96*x101 + 0.4*x96*x102 + 0.4*x96*x103 + 0.4*x96*x192 + 0.4*x97*x100 + 0.4*x97*x101 + 0.4*x97*x102 + 0.4*x97*x103 + 0.4*x97*x193 + 0.4*x98*x100 + 0.4*x98*x101 + 0.4*x98*x102 + 0.4*x98*x103 + 0.4*x98*x194 + 0.4*x99*x100 + 0.4*x99*x101 + 0.4*x99*x102 + 0.4*x99*x103 + 0.4*x99*x195 + 0.4*x100*x108 + 0.4*x101*x109 + 0.4*x102*x110 + 0.4*x103*x111 + 0.4*x104*x108 + 0.4*x104*x109 + 0.4*x104*x110 + 0.4*x104*x111 + 0.4*x104*x200 + 0.4*x105*x108 + 0.4*x105*x109 + 0.4*x105*x110 + 0.4*x105*x111 + 0.4*x105*x201 + 0.4*x106*x108 + 0.4*x106*x109 + 0.4*x106*x110 + 0.4*x106*x111 + 0.4*x106*x202 + 0.4*x107*x108 + 0.4*x107*x109 + 0.4*x107*x110 + 0.4*x107*x111 + 0.4*x107*x203 + 0.4*x108*x116 + 0.4*x109*x117 + 0.4*x110*x118 + 0.4*x111*x119 + 0.4*x112*x116 + 0.4*x112*x117 + 0.4*x112*x118 + 0.4*x112*x119 + 0.4*x112*x208 + 0.4*x113*x116 + 0.4*x113*x117 + 0.4*x113*x118 + 0.4*x113*x119 + 0.4*x113*x209 + 0.4*x114*x116 + 0.4*x114*x117 + 0.4*x114*x118 + 0.4*x114*x119 + 0.4*x114*x210 + 0.4*x115*x116 + 0.4*x115*x117 + 0.4*x115*x118 + 0.4*x115*x119 + 0.4*x115*x211 + 0.4*x192*x196 + 0.4*x192*x197 + 0.4*x192*x198 + 0.4*x192*x199 + 0.4*x193*x196 + 0.4*x193*x197 + 0.4*x193*x198 + 0.4*x193*x199 + 0.4*x194*x196 + 0.4*x194*x197 + 0.4*x194*x198 + 0.4*x194*x199 + 0.4*x195*x196 + 0.4*x195*x197 + 0.4*x195*x198 + 0.4*x195*x199 + 0.4*x196*x204 + 0.4*x197*x205 + 0.4*x198*x206 + 0.4*x199*x207 + 0.4*x200*x204 + 0.4*x200*x205 + 0.4*x200*x206 + 0.4*x200*x207 + 0.4*x201*x204 + 0.4*x201*x205 + 0.4*x201*x206 + 0.4*x201*x207 + 0.4*x202*x204 + 0.4*x202*x205 + 0.4*x202*x206 + 0.4*x202*x207 + 0.4*x203*x204 + 0.4*x203*x205 + 0.4*x203*x206 + 0.4*x203*x207 + 0.4*x204*x212 + 0.4*x205*x213 + 0.4*x206*x214 + 0.4*x207*x215 + 0.4*x208*x212 + 0.4*x208*x213 + 0.4*x208*x214 + 0.4*x208*x215 + 0.4*x209*x212 + 0.4*x209*x213 + 0.4*x209*x214 + 0.4*x209*x215 + 0.4*x210*x212 + 0.4*x210*x213 + 0.4*x210*x214 + 0.4*x210*x215 + 0.4*x211*x212 + 0.4*x211*x213 + 0.4*x211*x214 + 0.4*x211*x215;

solve minimize objective;

output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111, x112, x113, x114, x115, x116, x117, x118, x119, x192, x193, x194, x195, x196, x197, x198, x199, x200, x201, x202, x203, x204, x205, x206, x207, x208, x209, x210, x211, x212, x213, x214, x215])];
