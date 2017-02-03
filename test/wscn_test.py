import sys, os, json

sys.path.append('.')
import dwig

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

#print(data_dir)

class TestWSCNGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    def _json_comp(self, capfd, ground_truth_file, cli_args):
        with open(os.path.join(data_dir, ground_truth_file)) as file:
            ground_truth = json.load(file)

        dwig.main(self.parser.parse_args(cli_args))

        resout, reserr = capfd.readouterr()

        json_output = json.loads(resout)
        assert(ground_truth == json_output)


    #../dwig.py -cd 6 -rs 0 wscn > data/wscn_i_1.json
    def test_ran1_i_1(self, capfd):
        self._json_comp(capfd, 'wscn_i_1.json', ['-cd', '6', '-rs', '0', 'wscn'])

    #../dwig.py -cd 9 -rs 0 wscn > data/wscn_i_2.json
    def test_ran1_b_1(self, capfd):
        self._json_comp(capfd, 'wscn_i_2.json', ['-cd', '9', '-rs', '0', 'wscn'])

    #../dwig.py -cd 12 -rs 0 wscn > data/wscn_i_3.json
    def test_ran1_i_2(self, capfd):
        self._json_comp(capfd, 'wscn_i_3.json', ['-cd', '12', '-rs', '0', 'wscn'])



