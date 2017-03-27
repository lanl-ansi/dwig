import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestFLGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 2 -tl -rs 0 fl > data/fl_i_1.json
    def test_fl_i_1(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_1.json', ['-pp', '-cd', '2', '-tl', '-rs', '0', 'fl'])

    #../dwig.py -pp -cd 2 -tl -rs 0 fl -s 4 -a 0.3 > data/fl_i_2.json
    def test_fl_i_2(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_2.json', ['-pp', '-cd', '2', '-tl', '-rs', '0', 'fl', '-s', '4', '-a', '0.3'])

    #../dwig.py -pp -cd 2 -tl -rs 0 fl -mc -mll 0 > data/fl_i_3.json
    def test_fl_i_3(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_3.json', ['-pp', '-cd', '2', '-tl', '-rs', '0', 'fl', '-mc', '-mll', '0'])

    #../dwig.py -pp -cd 12 -tl -rs 0 fl > data/fl_i_4.json
    def test_fl_i_4(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_4.json', ['-pp', '-cd', '12', '-tl', '-rs', '0', 'fl'])
