import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestWSCNGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 6 -tl -rs 0 wscn > data/wscn_i_1.json
    def test_ran1_i_1(self, capfd):
        json_comp(self.parser, capfd, 'wscn_i_1.json', ['-pp', '-cd', '6', '-tl', '-rs', '0', 'wscn'])

    #../dwig.py -pp -cd 9 -tl -rs 0 wscn > data/wscn_i_2.json
    def test_ran1_b_1(self, capfd):
        json_comp(self.parser, capfd, 'wscn_i_2.json', ['-pp', '-cd', '9', '-tl', '-rs', '0', 'wscn'])

    #../dwig.py -pp -cd 12 -tl -rs 0 wscn > data/wscn_i_3.json
    def test_ran1_i_2(self, capfd):
        json_comp(self.parser, capfd, 'wscn_i_3.json', ['-pp', '-cd', '12', '-tl', '-rs', '0', 'wscn'])



