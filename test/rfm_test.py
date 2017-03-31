import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestRFMGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm > data/rfm1_i_1.json
    def test_rfm_i_1(self, capfd):
        json_comp(self.parser, capfd, 'rfm1_i_1.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'rfm'])

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm -f > data/rfm1_i_2.json
    def test_rfm1_i_2(self, capfd):
        json_comp(self.parser, capfd, 'rfm1_i_2.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'rfm', '-f'])

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm -f -s 4 > data/rfm4_i_1.json
    def test_rfm3_i_1(self, capfd):
        json_comp(self.parser, capfd, 'rfm4_i_1.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'rfm', '-f', '-s', '4'])
