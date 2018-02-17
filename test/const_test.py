import sys

sys.path.append('.')
import dwig

from common_test import json_comp
from common_test import run_dwig_cli


class TestConstGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -pp -cd  1 -tl -rs 0 -os const > data/const_i_1.json
    def test_const_i_1(self, capfd):
        json_comp(self.parser, capfd, 'const_i_1.json', ['-ic', '-pp','-cd', '1', '-tl', '-rs', '0', '-os', 'const'])

    #../dwig.py -pp -cd  1 -tl -rs 0 -os const -cp 0.2 > data/const_i_2.json
    def test_const_i_2(self, capfd):
        json_comp(self.parser, capfd, 'const_i_2.json', ['-ic', '-pp', '-cd', '1', '-tl', '-rs', '0', '-os', 'const', '-cp', '0.2'])

    #../dwig.py -pp -cd  1 -tl -rs 0 -os const -cp 0.2 -f -0.5 > data/const_i_3.json
    def test_const_i_3(self, capfd):
        json_comp(self.parser, capfd, 'const_i_3.json', ['-ic', '-pp', '-cd', '1', '-tl', '-rs', '0', '-os', 'const', '-cp', '0.2', '-f', '-0.5'])

    #../dwig.py -pp -cd 12 -tl -rs 0 -os const -cp 0.2 -f -0.5 > data/const_i_4.json
    def test_const_i_4(self, capfd):
        json_comp(self.parser, capfd, 'const_i_4.json', ['-ic', '-pp', '-cd', '12', '-tl', '-rs', '0', '-os', 'const', '-cp', '0.2', '-f', '-0.5'])

    #../dwig.py -pp -ccb 1 1 2 5 -tl -rs 0 -os const -cp 0.2 -f -0.5 > data/const_i_5.json
    def test_const_i_5(self, capfd):
        json_comp(self.parser, capfd, 'const_i_5.json', ['-ic', '-pp', '-ccb', '1', '1', '2', '5', '-tl', '-rs', '0', '-os', 'const', '-cp', '0.2', '-f', '-0.5'])



