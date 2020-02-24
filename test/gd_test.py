import sys

sys.path.append('.')
import dwig

from common_test import json_comp

class TestGDGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -ic -pp -cd  2 -tl -rs 0 gd > data/gd_i_1.json
    def test_gd_i_1(self, capfd):
        json_comp(self.parser, capfd, 'gd_i_1.json', ['-ic', '-pp', '-cd', '2', '-tl', '-rs', '0', 'gd'])

    #../dwig.py -ic -pp -cd  2 -tl -rs 0 gd -cval -1 0.2 -cpr 0.625 0.375 -fval -2.0 0.01 -fpr 0.01 0.99 > data/gd_i_2.json
    def test_gd_i_2(self, capfd):
        json_comp(self.parser, capfd, 'gd_i_2.json', ['-ic', '-pp', '-cd', '2', '-tl', '-rs', '0', 'gd', '-cval', '-1', '0.2', '-cpr', '0.625', '0.375', '-fval', '-2.0', '0.01', '-fpr', '0.01', '0.99'])

    #../dwig.py -ic -pp -cd  2 -tl -rs 0 gd -cval -1 0.2 -cpr 0.625 0.375 -fval -2.0 0.01 -fpr 0.01 0.99 -rgt > data/gd_i_3.json
    def test_gd_i_3(self, capfd):
        json_comp(self.parser, capfd, 'gd_i_3.json', ['-ic', '-pp', '-cd', '2', '-tl', '-rs', '0', 'gd', '-cval', '-1', '0.2', '-cpr', '0.625', '0.375', '-fval', '-2.0', '0.01', '-fpr', '0.01', '0.99', '-rgt'])

    #../dwig.py -ic -pp -cd  2 -tl -rs 0 gd -cval -1 0.2 -cpr 0.625 0.375 -fval -2.0 0.05 0.0 -fpr 0.01 0.20 0.79 > data/gd_i_4.json
    def test_gd_i_4(self, capfd):
        json_comp(self.parser, capfd, 'gd_i_4.json', ['-ic', '-pp', '-cd', '2', '-tl', '-rs', '0', 'gd', '-cval', '-1', '0.2', '-cpr', '0.625', '0.375', '-fval', '-2.0', '0.05', '0.0', '-fpr', '0.01', '0.20', '0.79'])

    #../dwig.py -ic -pp -cd 16 -tl -rs 0 gd -cval -1 0 1 -cpr 0.40 0.20 0.40 -fval -0.1 0.0 0.1 -fpr 0.40 0.20 0.40 -rgt > data/gd_i_5.json
    def test_gd_i_5(self, capfd):
        json_comp(self.parser, capfd, 'gd_i_5.json', ['-ic', '-pp', '-cd', '16', '-tl', '-rs', '0', 'gd', '-cval', '-1', '0', '1', '-cpr', '0.40', '0.20', '0.40', '-fval', '-0.1', '0.0', '0.1', '-fpr', '0.40', '0.20', '0.40', '-rgt'])
