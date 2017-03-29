import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestFLGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 6 -tl -rs 0 fl -sgs -cc -a 0.1 > data/fcl_i_1.json
    def test_fl_i_1(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_1.json', ['-pp', '-cd', '6', '-tl', '-rs', '0', 'fl', '-sgs', '-cc', '-a', '0.1'])

    #../dwig.py -pp -cd 6 -tl -rs 0 fl -sgs -cc -s 4 > data/fcl_i_2.json
    def test_fl_i_2(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_2.json', ['-pp', '-cd', '6', '-tl', '-rs', '0', 'fl', '-sgs', '-cc', '-s', '4'])

    #../dwig.py -pp -cd 12 -tl -rs 1 fl -sgs -cc > data/fcl_i_3.json
    def test_fl_i_3(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_3.json', ['-pp', '-cd', '12', '-tl', '-rs', '1', 'fl', '-sgs', '-cc'])

