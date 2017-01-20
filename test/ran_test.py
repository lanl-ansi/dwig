import sys, os, json

sys.path.append('.')
import dwig

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

print(data_dir)

class TestRanGeneration:
    def setup_class(self):
        self.parser = dwig.build_cli_parser()

    def _json_comp(self, capfd, ground_truth_file, cli_args):
        with open(os.path.join(data_dir, ground_truth_file)) as file:
            ground_truth = json.load(file)

        dwig.main(self.parser.parse_args(cli_args))

        resout, reserr = capfd.readouterr()

        json_output = json.loads(resout)
        assert(ground_truth == json_output)

    #../dwig.py -cd 1 -rs 0 -form ising ran > data/ran1_i_1.json
    def test_ran1_i_1(self, capfd):
        self._json_comp(capfd, 'ran1_i_1.json', ['-cd', '1', '-rs', '0', 'ran'])

    #../dwig.py -cd 1 -rs 0 -form binary ran > data/ran1_b_1.json
    def test_ran1_b_1(self, capfd):
        self._json_comp(capfd, 'ran1_b_1.json', ['-cd', '1', '-rs', '0', '-form', 'binary', 'ran'])

    #../dwig.py -cd 1 -rs 0 -form ising ran -f > data/ran1_i_2.json
    def test_ran1_i_2(self, capfd):
        self._json_comp(capfd, 'ran1_i_2.json', ['-cd', '1', '-rs', '0', 'ran', '-f'])

    #../dwig.py -cd 1 -rs 0 -form ising ran -s 4 > data/ran4_i_0.json
    def test_ran4_i_0(self, capfd):
        self._json_comp(capfd, 'ran4_i_0.json', ['-cd', '1', '-rs', '0', 'ran', '-s', '4'])



