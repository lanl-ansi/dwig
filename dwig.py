#!/usr/bin/env python2

from __future__ import print_function

import sys, os, json, argparse, random, math, datetime

from dwave_sapi2.util import get_chimera_adjacency
from dwave_sapi2.remote import RemoteConnection

from structure import QPUAssignment
from structure import ChimeraQPU
from structure import Range

import generator
from common import print_err
from common import validate_bqp_data
from common import json_dumps_kwargs

DEFAULT_CONFIG_FILE = '_config'


def main(args, output_stream=sys.stdout):
    case = build_case(args)
    validate_bqp_data(case)
    if args.pretty_print:
        print(json.dumps(case, **json_dumps_kwargs), file=output_stream)
    else:
        print(json.dumps(case, sort_keys=True), file=output_stream)


def build_case(args):
    if not args.seed is None:
        print_err('setting random seed to: {}'.format(args.seed))
        random.seed(args.seed)

    qpu = get_qpu(args.dw_url, args.dw_token, args.dw_proxy, args.dw_solver_name, args.hardware_chimera_degree)
    #print_err(qpu)

    if args.chimera_degree != None:
        print_err('filtering QPU to chimera of degree {}'.format(args.chimera_degree))
        qpu = qpu.chimera_degree_filter(args.chimera_degree)

    if args.generator == 'ran':
        qpu_config = generator.generate_ran(qpu, args.probability, args.steps, args.field, args.simple_ground_state)
    elif args.generator == 'rfm':
        qpu_config = generator.generate_rfm(qpu, args.steps, args.field)
    elif args.generator == 'fl':
        qpu_config = generator.generate_fl(qpu, args.steps, args.alpha, args.multicell, args.cluster_cells, args.simple_ground_state, args.min_loop_length, args.loop_reject_limit, args.loop_sample_limit)
    elif args.generator == 'wscn':
        if qpu.chimera_degree_view < 6:
            print_err('weak-strong cluster networks require a qpu with chimera degree of at least 6, the given degree is {}.'.format(qpu.chimera_degree_view))
            quit()

        effective_chimera_degree = 3*int(math.floor(qpu.chimera_degree_view/3))
        if effective_chimera_degree != qpu.chimera_degree_view:
            print_err('the weak-strong cluster network will occupy a space of chimera degree {}.'.format(effective_chimera_degree))
        qpu = qpu.chimera_degree_filter(effective_chimera_degree)

        qpu_config = generator.generate_wscn(qpu, args.weak_field, args.strong_field)
    else:
        assert(False) # CLI failed

    #print_err(qpu_config)
    if args.omit_solution:
        if isinstance(qpu_config, QPUAssignment):
            qpu_config = qpu_config.qpu_config

    data = qpu_config.build_dict()

    data['description'] = 'This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the {} algorithm.'.format(args.generator)
    if not args.seed is None:
        data['description'] = data['description'] + '  A random number seed of {} was used.'.format(args.seed)

    data['metadata'] = build_metadata(args, qpu)

    return data


def build_metadata(args, qpu):
    metadata = {}
    if not args.dw_url is None:
        metadata['dw_url'] = args.dw_url
    if not args.dw_solver_name is None:
        metadata['dw_solver_name'] = args.dw_solver_name
    if not qpu.chip_id is None:
        metadata['dw_chip_id'] = qpu.chip_id

    metadata['chimera_cell_size'] = qpu.cell_size
    metadata['chimera_degree'] = qpu.chimera_degree
    
    metadata['dwig_generator'] = args.generator

    if not args.timeless:
        metadata['generated'] = str(datetime.datetime.utcnow())

    return metadata


def get_qpu(url, token, proxy, solver_name, hardware_chimera_degree):
    chip_id = None
    cell_size = 8

    if not url is None and not token is None and not solver_name is None:
        print_err('QPU connection details found, accessing "{}" at "{}"'.format(solver_name, url))
        if proxy is None: 
            remote_connection = RemoteConnection(url, token)
        else:
            remote_connection = RemoteConnection(url, token, proxy)

        solver = remote_connection.get_solver(solver_name)

        couplers = solver.properties['couplers']

        couplers = set([tuple(coupler) for coupler in couplers])

        sites = solver.properties['qubits']

        solver_chimera_degree = int(math.ceil(math.sqrt(len(sites)/cell_size)))
        if hardware_chimera_degree != solver_chimera_degree:
            print_err('Warning: the hardware chimera degree was specified as {}, while the solver {} has a degree of {}'.format(hardware_chimera_degree, solver_name, solver_chimera_degree))

        site_range = Range(*solver.properties['h_range'])
        coupler_range = Range(*solver.properties['j_range'])
        chip_id = solver.properties['chip_id']

    else:
        print_err('QPU connection details not found, assuming full yield square chimera of degree {}'.format(hardware_chimera_degree))

        site_range = Range(-2.0, 2.0)
        coupler_range = Range(-1.0, 1.0)

        # the hard coded 4 here assumes an 4x2 unit cell
        arcs = get_chimera_adjacency(hardware_chimera_degree, hardware_chimera_degree, cell_size/2)

        # turn arcs into couplers
        # this step is nessisary to be consistent with the solver.properties['couplers'] data
        couplers = []
        for i,j in arcs:
            assert(i != j)
            if i < j:
                couplers.append((i,j))
            else:
                couplers.append((j,i))
        couplers = set(couplers)


        sites = set([coupler[0] for coupler in couplers]+[coupler[1] for coupler in couplers])

    # sanity check on coupler consistency across both branches
    for i,j in couplers:
        assert(i < j)

    return ChimeraQPU(sites, couplers, cell_size, hardware_chimera_degree, site_range, coupler_range, chip_id=chip_id)


# loads a configuration file and sets up undefined CLI arguments
def load_config(args):
    config_file_path = args.config_file

    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as config_file:
            try:
                config_data = json.load(config_file)
                for key, value in config_data.items():
                    if isinstance(value, dict) or isinstance(value, list):
                        print('invalid value for configuration key "{}", only single values are allowed'.format(config_file_path))
                        quit()
                    if not hasattr(args, key) or getattr(args, key) == None:
                        if isinstance(value, unicode):
                            value = value.encode('ascii','ignore')
                        setattr(args, key, value)
                    else:
                        print('skipping the configuration key "{}", it already has a value of {}'.format(key, str(getattr(args, key))))
                    #print(key, value)
            except ValueError:
                print('the config file does not appear to be a valid json document: {}'.format(config_file_path))
                quit()
    else:
        if config_file_path != DEFAULT_CONFIG_FILE:
            print('unable to open conifguration file: {}'.format(config_file_path))
            quit()

    return args


def build_cli_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-cf', '--config-file', help='a configuration file for specifying common parameters', default=DEFAULT_CONFIG_FILE)

    parser.add_argument('-url', '--dw-url', help='url of the d-wave machine')
    parser.add_argument('-token', '--dw-token', help='token for accessing the d-wave machine')
    parser.add_argument('-proxy', '--dw-proxy', help='proxy for accessing the d-wave machine')
    parser.add_argument('-solver', '--dw-solver-name', help='d-wave solver to use', type=int)


    parser.add_argument('-tl', '--timeless', help='omit generation timestamp', action='store_true', default=False)
    parser.add_argument('-rs', '--seed', help='seed for the random number generator', type=int)
    parser.add_argument('-cd', '--chimera-degree', help='the size of a square chimera graph to utilize', type=int)
    parser.add_argument('-hcd', '--hardware-chimera-degree', help='the size of the square chimera graph on the hardware', type=int, default=12)
    parser.add_argument('-pp', '--pretty-print', help='pretty print json output', action='store_true', default=False)
    parser.add_argument('-os', '--omit-solution', help='omit any solutions produced by the problem generator', action='store_true', default=False)


    subparsers = parser.add_subparsers()

    parser_ran = subparsers.add_parser('ran', help='generates a random problem')
    parser_ran.set_defaults(generator='ran')
    parser_ran.add_argument('-pr', '--probability', help='the probability that a coupling or field agrees with the planted ground state', type=float, default=0.5)
    parser_ran.add_argument('-s', '--steps', help='the number of steps in random numbers', type=int, default=1)
    parser_ran.add_argument('-f', '--field', help='include a random field', action='store_true', default=False)
    parser_ran.add_argument('-sgs', '--simple-ground-state', help='makes the planted ground state be all spins -1', action='store_true', default=False)

    parser_fl = subparsers.add_parser('fl', help='generates a frustrated loop problem')
    parser_fl.set_defaults(generator='fl')
    parser_fl.add_argument('-s', '--steps', help='the number of allowed steps in output Hamiltonian', type=int, default=2)
    parser_fl.add_argument('-a', '--alpha', help='site-to-loop ratio', type=float, default=0.2)
    parser_fl.add_argument('-mc', '--multicell', help='reject loops that are within one chimera cell', action='store_true', default=False)
    parser_fl.add_argument('-cc', '--cluster-cells', help='treats each chimera cell as a single logical spin', action='store_true', default=False)
    parser_fl.add_argument('-sgs', '--simple-ground-state', help='makes the planted ground state be all spins -1', action='store_true', default=False)
    parser_fl.add_argument('-mll', '--min-loop-length', help='the minimum length of a loop', type=int, default=7)
    parser_fl.add_argument('-lrl', '--loop-reject-limit', help='the maximum amount of loops to be reject', type=int, default=1000)
    parser_fl.add_argument('-lsl', '--loop-sample-limit', help='the maximum amount of random walk samples', type=int, default=10000)

    parser_wscn = subparsers.add_parser('wscn', help='generates a weak-strong cluster network problem')
    parser_wscn.set_defaults(generator='wscn')
    parser_wscn.add_argument('-wf', '--weak-field', help='strength of the weak field', type=float, default=0.44)
    parser_wscn.add_argument('-sf', '--strong-field', help='strength of the weak field', type=float, default=-1)


    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(load_config(parser.parse_args()))
