#!/usr/bin/env python2

import sys, os, json, argparse, random, math

from dwave_sapi2.util import get_chimera_adjacency
from dwave_sapi2.remote import RemoteConnection

from structure import ChimeraQPU
from structure import QPUConfiguration

DEFAULT_CHIMERA_DEGREE = 12
DEFAULT_CONFIG_FILE = '_config'


def main(args):
    if not args.seed is None:
        random.seed(args.seed)

    sites, couplers, chimera_degree = get_qpu_specs(args.dw_url, args.dw_token, args.dw_proxy, args.solver_name, args.chimera_degree)

    qpu = ChimeraQPU(sites, couplers, chimera_degree)
    print_err(qpu)

    if args.chimera_degree != None:
        qpu = qpu.chimera_degree_filter(args.chimera_degree)
        print_err(qpu)

    qpu_config = ran_generator(qpu, steps = 1)

    print_err(qpu_config)

    if args.qubist_hamiltonian:
        print(qpu_config.qubist_hamiltonian())

def get_qpu_specs(url=None, token=None, proxy=None, solver_name=None, chimera_degree=None):
    if not url is None and not token is None and not solver_name is None:
        print_err('QPU connection details found, accessing "%s" at "%s"' % (solver_name, url))
        if proxy is None: 
            remote_connection = RemoteConnection(url, token)
        else:
            remote_connection = RemoteConnection(url, token, proxy)

        solver = remote_connection.get_solver(solver_name)

        couplers = solver.properties['couplers']

        couplers = set([tuple(coupler) for coupler in couplers])
        sites = solver.properties['qubits']

        chimera_degree = int(math.ceil(math.sqrt(len(sites)/8.0)))
        print_err('inferred square chimera of degree %d on "%s"' % (chimera_degree, solver_name))

    else:
        chimera_degree = DEFAULT_CHIMERA_DEGREE
        if chimera_degree == None:
            chimera_degree = DEFAULT_CHIMERA_DEGREE

        print_err('QPU connection details not found, assuming full yield square chimera of degree %d' % chimera_degree)

        # the hard coded 4 here assumes an 4x2 unit cell
        arcs = get_chimera_adjacency(chimera_degree, chimera_degree, 4)

        # turn arcs into couplers
        couplers = []
        for i,j in arcs:
            assert(i != j)
            if i < j:
                couplers.append((i,j))
            else:
                couplers.append((j,i))
        couplers = set(couplers)

        sites = set([coupler[0] for coupler in couplers]+[coupler[1] for coupler in couplers])

    # sanity check on couplers
    for i,j in couplers:
        assert(i < j)

    return sites, couplers, chimera_degree


def ran_generator(qpu, steps = 1):
    couplings = {coupler : -1.0 if random.random() <= 0.5 else 1.0 for coupler in qpu.couplers}
    return QPUConfiguration(qpu, {}, couplings)


# prints a line to standard error
def print_err(data):
    sys.stderr.write(str(data)+'\n')

# loads a configuration file and sets up undefined CLI arguments
def load_config(args):
    config_file_path = args.config_file

    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as config_file:
            try:
                config_data = json.load(config_file)
                for key, value in config_data.items():
                    if isinstance(value, dict) or isinstance(value, list):
                        print('invalid value for configuration key "%s", only single values are allowed' % config_file_path)
                        quit()
                    if not hasattr(args, key) or getattr(args, key) == None:
                        if isinstance(value, unicode):
                            value = value.encode('ascii','ignore')
                        setattr(args, key, value)
                    else:
                        print('skipping the configuration key "%s", it already has a value of %s' % (key, str(getattr(args, key))))
                    #print(key, value)
            except ValueError:
                print('the config file does not appear to be a valid json document: %s' % config_file_path)
                quit()
    else:
        if config_file_path != DEFAULT_CONFIG_FILE:
            print('unable to open conifguration file: %s' % config_file_path)
            quit()

    return args

def build_cli_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-cf', '--config-file', help='a configuration file for specifing common parameters', default=DEFAULT_CONFIG_FILE)

    parser.add_argument('-url', '--dw-url', help='url of the d-wave machine')
    parser.add_argument('-token', '--dw-token', help='token for accessing the d-wave machine')
    parser.add_argument('-proxy', '--dw-proxy', help='proxy for accessing the d-wave machine')
    parser.add_argument('-solver', '--solver-name', help='d-wave solver to use', type=int)

    parser.add_argument('-cd', '--chimera-degree', help='the degree of the square chimera graph', type=int)
    #parser.add_argument('-o', '--output', help='the output file name')
    parser.add_argument('-dqh', '--qubist-hamiltonian', help='prints a Hamiltonian to stdout that can be read by qubist', action='store_true')
    
    parser.add_argument('-rs', '--seed', help='seed for the random number generator', type=int)
    #parser.add_argument('-dqp', '--display-qaudratic-program', help='prints the qaudratic program to stdout', action='store_true', default=False)
    #parser.add_argument('-rtl', '--runtime-limit', help='gurobi runtime limit (sec.)', type=int)

    #parser.add_argument('-g', '--generator', choices=['ran1', 'negative', 'checker', 'frustrated-checker'], default='ran1')
    subparsers = parser.add_subparsers()

    parser_ran = subparsers.add_parser('ran', help='builds a ran-n problem')
    parser_ran.set_defaults(generator='ran')
    parser_ran.add_argument('-s', '--steps', help='the number of steps in random numbers', type=int, default=1)

    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(load_config(parser.parse_args()))
