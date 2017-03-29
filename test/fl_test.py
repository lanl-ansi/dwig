import sys

sys.path.append('.')
import dwig

from common_test import json_comp
from common_test import run_dwig_cli


class TestFLGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 2 -tl -rs 0 fl -sgs > data/fl_i_1.json
    def test_fl_i_1(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_1.json', ['-pp', '-cd', '2', '-tl', '-rs', '0', 'fl', '-sgs'])

    #../dwig.py -pp -cd 2 -tl -rs 0 fl -sgs -s 4 -a 0.3 > data/fl_i_2.json
    def test_fl_i_2(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_2.json', ['-pp', '-cd', '2', '-tl', '-rs', '0', 'fl', '-sgs', '-s', '4', '-a', '0.3'])

    #../dwig.py -pp -cd 2 -tl -rs 0 fl -sgs -mc -mll 0 > data/fl_i_3.json
    def test_fl_i_3(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_3.json', ['-pp', '-cd', '2', '-tl', '-rs', '0', 'fl', '-sgs', '-mc', '-mll', '0'])

    #../dwig.py -pp -cd 12 -tl -rs 0 fl -sgs > data/fl_i_4.json
    def test_fl_i_4(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_4.json', ['-pp', '-cd', '12', '-tl', '-rs', '0', 'fl', '-sgs'])

    #../dwig.py -pp -cd  2 -tl -rs 0 fl > data/fl_i_5.json
    def test_fl_i_5(self, capfd):
        json_comp(self.parser, capfd, 'fl_i_5.json', ['-pp', '-cd', '2', '-tl', '-rs', '0', 'fl'])


class TestFLGroundState:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd 2 -tl -rs 0 fl -sgs > data/fl_i_1.json
    def test_eq(self, capfd):
        cli_args = ['-cd', '2', '-tl', '-rs', '0', 'fl']

        json_base = run_dwig_cli(self.parser, cli_args)

        cli_args.append('-sgs')
        json_sgs = run_dwig_cli(self.parser, cli_args)

        base_solution_eval = json_base['solutions'][0]['evaluation']
        sgs_solution_eval = json_sgs['solutions'][0]['evaluation']
        assert(abs(base_solution_eval - sgs_solution_eval) <= 1e-8)
