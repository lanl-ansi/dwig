import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestFLGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -cd 6 -tl -rs 0 fl -cc -a 0.1 > data/fcl_i_1.json
    def test_fl_i_1(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_1.json', ['-cd', '6', '-tl', '-rs', '0', 'fl', '-cc', '-a', '0.1'])

    #../dwig.py -cd 6 -tl -rs 0 fl -cc -s 4 > data/fcl_i_2.json
    def test_fl_i_2(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_2.json', ['-cd', '6', '-tl', '-rs', '0', 'fl', '-cc', '-s', '4'])

    #../dwig.py -cd 12 -tl -rs 1 fl -cc > data/fcl_i_3.json
    def test_fl_i_3(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_3.json', ['-cd', '12', '-tl', '-rs', '1', 'fl', '-cc'])

