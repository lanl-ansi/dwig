import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestWSCNGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -cd 6 -tl -rs 0 wscn > data/wscn_i_1.json
    def test_ran1_i_1(self, capfd):
        json_comp(self.parser, capfd, 'wscn_i_1.json', ['-cd', '6', '-tl', '-rs', '0', 'wscn'])

    #../dwig.py -cd 9 -tl -rs 0 wscn > data/wscn_i_2.json
    def test_ran1_b_1(self, capfd):
        json_comp(self.parser, capfd, 'wscn_i_2.json', ['-cd', '9', '-tl', '-rs', '0', 'wscn'])

    #../dwig.py -cd 12 -tl -rs 0 wscn > data/wscn_i_3.json
    def test_ran1_i_2(self, capfd):
        json_comp(self.parser, capfd, 'wscn_i_3.json', ['-cd', '12', '-tl', '-rs', '0', 'wscn'])



