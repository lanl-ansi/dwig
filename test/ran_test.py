import sys, os, json

sys.path.append('.')
import dwpg

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

print(data_dir)

class TestRanGeneration:
    def setup_class(self):
        self.parser = dwpg.build_cli_parser()


    def test_ran1_i_0_qh(self, capfd):
        #../dwpg.py -cd 1 -rs 0 ran > data/ran1_i_0.qh
        with open(os.path.join(data_dir, 'ran1_i_0.qh')) as file:
            ground_truth = file.read()

        dwpg.main(self.parser.parse_args(['-cd', '1', '-rs', '0', 'ran']))

        resout, reserr = capfd.readouterr()
        
        #print(ground_truth == resout)
        assert(ground_truth == resout)

    def _json_comp(self, capfd, ground_truth_file, cli_args):
        with open(os.path.join(data_dir, ground_truth_file)) as file:
            ground_truth = json.load(file)

        dwpg.main(self.parser.parse_args(cli_args))

        resout, reserr = capfd.readouterr()

        json_output = json.loads(resout)
        assert(ground_truth == json_output)

    #../dwpg.py -cd 1 -rs 0 -form ising ran > data/ran1_i_1.json
    def test_ran1_i_1(self, capfd):
        self._json_comp(capfd, 'ran1_i_1.json', ['-cd', '1', '-rs', '0', '-form', 'ising', 'ran'])

    #../dwpg.py -cd 1 -rs 0 -form binary ran > data/ran1_b_1.json
    def test_ran1_b_1(self, capfd):
        self._json_comp(capfd, 'ran1_b_1.json', ['-cd', '1', '-rs', '0', '-form', 'binary', 'ran'])

    #../dwpg.py -cd 1 -rs 0 -form ising ran -f > data/ran1_i_2.json
    def test_ran1_i_2(self, capfd):
        self._json_comp(capfd, 'ran1_i_2.json', ['-cd', '1', '-rs', '0', '-form', 'ising', 'ran', '-f'])

    #../dwpg.py -cd 1 -rs 0 -form ising ran -s 4 > data/ran4_i_0.json
    def test_ran4_i_0(self, capfd):
        self._json_comp(capfd, 'ran4_i_0.json', ['-cd', '1', '-rs', '0', '-form', 'ising', 'ran', '-s', '4'])



