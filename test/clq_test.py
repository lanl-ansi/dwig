import sys

sys.path.append('.')
import dwig

from common_test import json_comp

class TestFLGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    #../dwig.py -cd 1 -rs 0 clq > data/clq_i_1.json
    def test_clq_i_1(self, capfd):
        json_comp(self.parser, capfd, 'clq_i_1.json', ['-cd', '1', '-rs', '0', 'clq'])

    #../dwig.py -cd 2 -rs 0 clq > data/clq_i_2.json
    def test_clq_i_2(self, capfd):
        json_comp(self.parser, capfd, 'clq_i_2.json', ['-cd', '2', '-rs', '0', 'clq'])

    #../dwig.py -cd 3 -rs 0 clq > data/clq_i_3.json
    def test_clq_i_3(self, capfd):
        json_comp(self.parser, capfd, 'clq_i_3.json', ['-cd', '3', '-rs', '0', 'clq'])

