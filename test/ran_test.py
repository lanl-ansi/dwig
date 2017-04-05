import sys

sys.path.append('.')
import dwig

from common_test import json_comp
from common_test import run_dwig_cli


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
        json_comp(self.parser, capfd, 'rfm1_i_1.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'ran', '-pr', '1.0'])

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm -f > data/rfm1_i_2.json
    def test_rfm1_i_2(self, capfd):
        json_comp(self.parser, capfd, 'rfm1_i_2.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'ran', '-f', '-pr', '1.0'])

    #../dwig.py -pp -cd 1 -tl -rs 0 rfm -f -s 4 > data/rfm4_i_1.json
    def test_rfm3_i_1(self, capfd):
        json_comp(self.parser, capfd, 'rfm4_i_1.json', ['-pp', '-cd', '1', '-tl', '-rs', '0', 'ran', '-f', '-s', '4', '-pr', '1.0'])


class TestRANGroundState:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    def test_sgs(self, capfd):
        cli_args = ['-cd', '2', '-tl', '-rs', '0', 'ran', '-sgs', '-pr', '1.0']

        json_base = run_dwig_cli(self.parser, cli_args)

        for lt in json_base['linear_terms']:
            assert(lt['coeff'] == 0.0)

        for qt in json_base['quadratic_terms']:
            assert(qt['coeff'] <= -1.0)

    def test_sgs_feild(self, capfd):
        cli_args = ['-cd', '2', '-tl', '-rs', '0', 'ran', '-sgs', '-f', '-pr', '1.0']

        json_base = run_dwig_cli(self.parser, cli_args)

        for lt in json_base['linear_terms']:
            assert(lt['coeff'] >= 1.0)

        for qt in json_base['quadratic_terms']:
            assert(qt['coeff'] <= -1.0)

