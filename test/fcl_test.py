import sys

sys.path.append('.')
import dwig

from common_test import json_comp
from common_test import run_dwig_cli


class TestFCLGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 6 -tl -rs 0 fl -sgs -ccc -a 0.1 > data/fcl_i_1.json
    def test_fcl_i_1(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_1.json', ['-ic', '-pp', '-cd', '6', '-tl', '-rs', '0', 'fl', '-sgs', '-ccc', '-a', '0.1'])

    #../dwig.py -pp -cd 6 -tl -rs 0 fl -sgs -ccc -s 4 > data/fcl_i_2.json
    def test_fcl_i_2(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_2.json', ['-ic', '-pp', '-cd', '6', '-tl', '-rs', '0', 'fl', '-sgs', '-ccc', '-s', '4'])

    #../dwig.py -pp -cd 12 -tl -rs 1 fl -sgs -ccc > data/fcl_i_3.json
    def test_fcl_i_3(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_3.json', ['-ic', '-pp', '-cd', '16', '-tl', '-rs', '1', 'fl', '-sgs', '-ccc'])

    #../dwig.py -pp -cd 6 -tl -rs 0 fl -ccc -a 0.1 > data/fcl_i_4.json
    def test_fcl_i_4(self, capfd):
        json_comp(self.parser, capfd, 'fcl_i_4.json', ['-ic', '-pp', '-cd', '6', '-tl', '-rs', '0', 'fl', '-ccc', '-a', '0.1'])


class TestFCLGroundState:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 6 -tl -rs 0 fl -sgs -ccc -a 0.1 > data/fcl_i_1.json
    def test_eq(self, capfd):
        cli_args = ['-ic', '-pp', '-cd', '6', '-tl', '-rs', '0', 'fl', '-ccc', '-a', '0.1']

        json_base = run_dwig_cli(self.parser, cli_args)

        cli_args.append('-sgs')
        json_sgs = run_dwig_cli(self.parser, cli_args)

        base_solution_eval = json_base['solutions'][0]['evaluation']
        sgs_solution_eval = json_sgs['solutions'][0]['evaluation']
        assert(abs(base_solution_eval - sgs_solution_eval) <= 1e-8)
