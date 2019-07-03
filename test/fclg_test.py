import sys

sys.path.append('.')
import dwig

from common_test import json_comp
from common_test import run_dwig_cli


class TestFclgGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()
    
    # ../dwig.py -ic -pp -cd 12 -tl -rs 0 fclg -gf 0.1 -mll 5 -a 0.1 > data/fclg_i_1.json
    def test_fclg_i_1(self, capfd):
        json_comp(self.parser, capfd, 'fclg_i_1.json', ['-ic', '-pp', '-cd', '12', '-tl', '-rs', '0', 'fclg', '-gf', '0.1', '-mll', '5', '-a', '0.1'])

    # ../dwig.py -ic -pp -cd 13 -tl -rs 0 fclg -gf 0.2 > data/fclg_i_2.json
    def test_fclg_i_2(self, capfd):
        json_comp(self.parser, capfd, 'fclg_i_2.json', ['-ic', '-pp', '-cd', '13', '-tl', '-rs', '0', 'fclg', '-gf', '0.2'])

    # ../dwig.py -ic -pp -cd 14 -tl -rs 0 fclg -gf 0.3 -mll 0 > data/fclg_i_3.json
    def test_fclg_i_3(self, capfd):
        json_comp(self.parser, capfd, 'fclg_i_3.json', ['-ic', '-pp', '-cd', '14', '-tl', '-rs', '0', 'fclg', '-gf', '0.3', '-mll', '0'])

    # ../dwig.py -ic -pp -cd 15 -tl -rs 0 fclg -gf 0.4 -sgs -s 2 > data/fclg_i_4.json
    def test_fclg_i_4(self, capfd):
        json_comp(self.parser, capfd, 'fclg_i_4.json', ['-ic', '-pp', '-cd', '15', '-tl', '-rs', '0', 'fclg', '-gf', '0.4', '-sgs', '-s', '2'])

    # ../dwig.py -ic -pp -cd 16 -tl -rs 0 fclg -gf 0.5 -sgs > data/fclg_i_5.json
    def test_fclg_i_5(self, capfd):
        json_comp(self.parser, capfd, 'fclg_i_5.json', ['-ic', '-pp', '-cd', '16', '-tl', '-rs', '0', 'fclg', '-gf', '0.5', '-sgs'])


class TestFclgGroundState:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    # ../dwig.py -ic -pp -cd 12 -tl -rs 0 fclg -gf 0.1 -mll 5 -a 0.1 > data/fclg_i_1.json
    def test_eq(self, capfd):
        cli_args = ['-ic', '-pp', '-cd', '12', '-tl', '-rs', '0', 'fclg', '-gf', '0.1', '-mll', '5', '-a', '0.1']

        json_base = run_dwig_cli(self.parser, cli_args)

        cli_args.append('-sgs')
        json_sgs = run_dwig_cli(self.parser, cli_args)

        base_solution_eval = json_base['solutions'][0]['evaluation']
        sgs_solution_eval = json_sgs['solutions'][0]['evaluation']
        assert(abs(base_solution_eval - sgs_solution_eval) <= 1e-8)
