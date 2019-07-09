import sys

sys.path.append('.')
import dwig

from common_test import json_comp
from common_test import run_dwig_cli


class TestXranGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    # ../dwig.py -ic -pp -tl -rs 0 -cd 8 xran -cv " -5,-1,1" -cw 2,1,1 > data/xran_i_1.json
    def test_xran_i_1(self, capfd):
        json_comp(self.parser, capfd, 'xran_i_1.json', ['-ic', '-pp', '-tl', '-rs', '0', '-cd', '8', 'xran', '-cv',' -5,-1,1', '-cw', '2,1,1'])

    # ../dwig.py -ic -pp -tl -rs 0 -cd 12 xran -cv " -3,-1,1,3" -cw 7,1,1,7 > data/xran_i_2.json
    def test_xran_i_2(self, capfd):
        json_comp(self.parser, capfd, 'xran_i_2.json', ['-ic', '-pp', '-tl', '-rs', '0', '-cd', '12', 'xran', '-cv',' -3,-1,1,3', '-cw', '7,1,1,7'])

    # ../dwig.py -ic -pp -tl -rs 0 -cd 16 xran -cv " -1,-0.5,0,0.5,1" -cw 3,1.5,1,2,2.5 > data/xran_i_3.json
    def test_xran_i_3(self, capfd):
        json_comp(self.parser, capfd, 'xran_i_3.json', ['-ic', '-pp', '-tl', '-rs', '0', '-cd', '16', 'xran', '-cv',' -1,-0.5,0,0.5,1', '-cw', '3,1.5,1,2,2.5'])

    # ../dwig.py -ic -pp -tl -rs 0 -cd 16 xran -cv " -1,1" -cw 1,1 -f -fv " -1,1" -fw 1,1> data/xran_i_4.json
    def test_xran_i_4(self, capfd):
        json_comp(self.parser, capfd, 'xran_i_4.json', ['-ic', '-pp', '-tl', '-rs', '0', '-cd', '16', 'xran', '-cv',' -1,1', '-cw', '1,1', '-f', '-fv', ' -1,1', '-fw', '1,1'])

    # ../dwig.py -ic -pp -tl -rs 0 -cd 12 xran -cv 1,2,3,4 -cw 0,1,0,1 -f -fv " -3,4" -fw 1,2 > data/xran_i_5.json
    def test_xran_i_5(self, capfd):
        json_comp(self.parser, capfd, 'xran_i_5.json', ['-ic', '-pp', '-tl', '-rs', '0', '-cd', '12', 'xran', '-cv','1,2,3,4', '-cw', '0,1,0,1', '-f', '-fv', ' -3,4', '-fw', '1,2'])

    # ../dwig.py -ic -pp -tl -rs 0 -cd 8 xran -cv 4,3,2,1 -cw 0,0,1,2 -f -fv 3,2.5 -fw 5,1 > data/xran_i_6.json
    def test_xran_i_6(self, capfd):
        json_comp(self.parser, capfd, 'xran_i_6.json', ['-ic', '-pp', '-tl', '-rs', '0', '-cd', '8', 'xran', '-cv','4,3,2,1', '-cw', '0,0,1,2', '-f', '-fv', '3,2.5', '-fw', '5,1'])
