import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestCBFMGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -ic -pp -cd 6 -tl -rs 0 cbfm > data/cbfm_i_1.json
    def test_cbfm_i_1(self, capfd):
        json_comp(self.parser, capfd, 'cbfm_i_1.json', ['-ic', '-pp', '-cd', '6', '-tl', '-rs', '0', 'cbfm'])

    #../dwig.py -ic -pp -cd 9 -tl -rs 0 cbfm -rgt > data/cbfm_i_2.json
    def test_cbfm_i_2(self, capfd):
        json_comp(self.parser, capfd, 'cbfm_i_2.json', ['-ic', '-pp', '-cd', '9', '-tl', '-rs', '0', 'cbfm', '-rgt'])

    #../dwig.py -ic -pp -cd 12 -tl -rs 0 cbfm > data/cbfm_i_3.json
    def test_cbfm_i_3(self, capfd):
        json_comp(self.parser, capfd, 'cbfm_i_3.json', ['-ic', '-pp', '-cd', '12', '-tl', '-rs', '0', 'cbfm'])

    #../dwig.py -ic -pp -cd 16 -tl -rs 0 cbfm -rgt > data/cbfm_i_4.json
    def test_cbfm_i_4(self, capfd):
        json_comp(self.parser, capfd, 'cbfm_i_4.json', ['-ic', '-pp', '-cd', '16', '-tl', '-rs', '0', 'cbfm', '-rgt'])

