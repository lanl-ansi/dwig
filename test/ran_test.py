import sys

sys.path.append('.')
import dwig

from common_test import json_comp


class TestRanGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 1 -tl -rs 0 -form ising ran > data/ran1_i_1.json
    def test_ran1_i_1(self, capfd):
        json_comp(self.parser, capfd, 'ran1_i_1.json', ['-pp','-cd', '1', '-tl', '-rs', '0', '-os', 'ran'])

    #../dwig.py -pp -cd 1 -tl -rs 0 -form ising ran -f > data/ran1_i_2.json
    def test_ran1_i_2(self, capfd):
        json_comp(self.parser, capfd, 'ran1_i_2.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', '-os', 'ran', '-f'])

    #../dwig.py -pp -cd 1 -tl -rs 0 -form ising ran -s 4 > data/ran4_i_0.json
    def test_ran4_i_0(self, capfd):
        json_comp(self.parser, capfd, 'ran4_i_0.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', '-os', 'ran', '-s', '4'])

    #../dwig.py -pp -cd 12 -tl -rs 0 ran > data/ran1_i_3.json
    def test_ran1_i_3(self, capfd):
        json_comp(self.parser, capfd, 'ran1_i_3.json', ['-pp', '-cd', '12', '-tl', '-rs', '0', '-os', 'ran'])



class TestRFMGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm > data/rfm1_i_1.json
    def test_rfm_i_1(self, capfd):
        json_comp(self.parser, capfd, 'rfm1_i_1.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'ran', '-a', '0.0'])

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm -f > data/rfm1_i_2.json
    def test_rfm1_i_2(self, capfd):
        json_comp(self.parser, capfd, 'rfm1_i_2.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'ran', '-f', '-a', '0.0'])

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm -f -s 4 > data/rfm4_i_1.json
    def test_rfm3_i_1(self, capfd):
        json_comp(self.parser, capfd, 'rfm4_i_1.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'ran', '-f', '-s', '4', '-a', '0.0'])
