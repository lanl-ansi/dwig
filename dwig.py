#!/usr/bin/env python3

from __future__ import print_function

import sys, os, json, argparse, random, math, datetime

from dwave.cloud import Client
import dwave_networkx

from structure import QPUAssignment
from structure import ChimeraQPU
from structure import Range

import generator
from common import print_err
from common import validate_bqp_data
from common import json_dumps_kwargs

# caches remote qpu info when making multiple calls to build_case
_qpu_remote = None

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

    qpu = get_qpu(args.profile, args.ignore_connection, args.hardware_chimera_degree)
    #print_err(qpu)

    if args.chimera_degree != None:
        print_err('filtering QPU to chimera of degree {}'.format(args.chimera_degree))
        qpu = qpu.chimera_degree_filter(args.chimera_degree)

    if args.chimera_cell_limit != None:
        print_err('filtering QPU to the first {} chimera cells'.format(args.chimera_cell_limit))
        qpu = qpu.cell_filter(args.chimera_cell_limit)

    if args.chimera_cell_box != None:
        chimera_cell_1 = tuple(args.chimera_cell_box[0:2])
        chimera_cell_2 = tuple(args.chimera_cell_box[2:4])
        print_err('filtering QPU to the chimera cell box {} by {}'.format(chimera_cell_1, chimera_cell_2))
        qpu = qpu.chimera_cell_box_filter(chimera_cell_1, chimera_cell_2)

    if args.generator == 'const':
        qpu_config = generator.generate_disordered(qpu, [args.coupling], [1.0], [args.field], [1.0], args.random_gauge_transformation)
    elif args.generator == 'ran':
        qpu_config = generator.generate_ran(qpu, args.probability, args.steps, args.field, args.scale, args.simple_ground_state)
    elif args.generator == 'gd':
        qpu_config = generator.generate_disordered(qpu, args.coupling_values, args.coupling_probabilities, args.field_values, args.field_probabilities, args.random_gauge_transformation)
    elif args.generator == 'cbfm':
        qpu_config = generator.generate_disordered(qpu, [args.j1_val, args.j2_val], [args.j1_pr, args.j2_pr], [args.h1_val, args.h2_val], [args.h1_pr, args.h2_pr], args.random_gauge_transformation)
    elif args.generator == 'fl':
        qpu_config = generator.generate_fl(qpu, args.steps, args.alpha, args.multicell, args.cluster_chimera_cells, args.simple_ground_state, args.min_loop_length, args.loop_reject_limit, args.loop_sample_limit)
    elif args.generator == 'wscn':
        if args.chimera_cell_limit != None:
            print_err('weak-strong cluster networks cannot be constricted with a cell limit.')
            quit()

        if qpu.chimera_degree_view < 6:
            print_err('weak-strong cluster networks require a qpu with chimera degree of at least 6, the given degree is {}.'.format(qpu.chimera_degree_view))
            quit()

        effective_chimera_degree = 3*(qpu.chimera_degree_view//3)
        if effective_chimera_degree != qpu.chimera_degree_view:
            print_err('the weak-strong cluster network will occupy a space of chimera degree {}.'.format(effective_chimera_degree))
        qpu = qpu.chimera_degree_filter(effective_chimera_degree)

        qpu_config = generator.generate_wscn(qpu, args.weak_field, args.strong_field)
    elif args.generator == 'fclg':
        qpu_config = generator.generate_fclg(qpu, args.steps, args.alpha, args.gadget_fraction, args.simple_ground_state, args.min_loop_length, args.loop_reject_limit, args.loop_sample_limit)
    else:
        assert(False) # CLI failed

    if args.include_zeros:
        config = qpu_config
        if isinstance(qpu_config, QPUAssignment):
            config = qpu_config.qpu_config
        for site in config.qpu.sites:
            if not site in config.fields:
                config.fields[site] = 0.0
        for coupler in config.qpu.couplers:
            if not coupler in config.couplings:
                config.couplings[coupler] = 0.0

    #print_err(qpu_config)
    if args.omit_solution:
        if isinstance(qpu_config, QPUAssignment):
            qpu_config = qpu_config.qpu_config



    data = qpu_config.build_dict(args.include_zeros)

    data['description'] = 'This is a randomly generated B-QP built by D-WIG (https://github.com/lanl-ansi/dwig) using the {} algorithm.'.format(args.generator)
    if not args.seed is None:
        data['description'] = data['description'] + '  A random number seed of {} was used.'.format(args.seed)

    data['metadata'] = build_metadata(args, qpu)

    return data


def build_metadata(args, qpu):
    metadata = {}
    if not qpu.endpoint is None:
        metadata['dw_endpoint'] = qpu.endpoint
    if not qpu.solver_name is None:
        metadata['dw_solver_name'] = qpu.solver_name
    if not qpu.chip_id is None:
        metadata['dw_chip_id'] = qpu.chip_id

    metadata['chimera_cell_size'] = qpu.cell_size
    metadata['chimera_degree'] = qpu.chimera_degree

    metadata['dwig_generator'] = args.generator

    if not args.timeless:
        metadata['generated'] = str(datetime.datetime.utcnow())

    return metadata


def get_qpu(profile, ignore_connection, hardware_chimera_degree):
    chip_id = None
    endpoint = None
    solver_name = None
    cell_size = 8

    global _qpu_remote

    if not ignore_connection:
        if _qpu_remote == None:
            try:
                with Client.from_config(config_file=os.getenv("HOME")+"/dwave.conf", profile=profile) as client:
                    endpoint = client.endpoint
                    solver = client.get_solver()
                    solver_name = solver.name
                    couplers = solver.undirected_edges
                    sites = solver.nodes

                    solver_chimera_degree = int(math.ceil(math.sqrt(len(sites)/cell_size)))
                    if hardware_chimera_degree != solver_chimera_degree:
                        print_err('Warning: the hardware chimera degree was specified as {}, while the solver {} has a degree of {}'.format(hardware_chimera_degree, solver_name, solver_chimera_degree))
                        hardware_chimera_degree = solver_chimera_degree

                    site_range = Range(*solver.properties['h_range'])
                    coupler_range = Range(*solver.properties['j_range'])
                    chip_id = solver.properties['chip_id']

            #TODO remove try/except logic, if there is a better way to check the connection
            except Exception as e:
               print_err('QPU connection details not found or there was a connection error')
               print_err('  '+str(e))
               print_err('assuming full yield square chimera of degree {}'.format(hardware_chimera_degree))
               ignore_connection = True
        else:
            print_err('info: using cached QPU details')
            return _qpu_remote

    if ignore_connection:
        site_range = Range(-2.0, 2.0)
        coupler_range = Range(-1.0, 1.0)

        # the hard coded 4 here assumes an 4x2 unit cell
        graph = dwave_networkx.chimera_graph(hardware_chimera_degree, hardware_chimera_degree, cell_size//2)
        edges = graph.edges()
        #arcs = get_chimera_adjacency(hardware_chimera_degree, hardware_chimera_degree, cell_size//2)
        #print(arcs)

        # turn arcs into couplers
        # this step is nessisary to be consistent with the solver.properties['couplers'] data
        couplers = []
        for i,j in edges:
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

    if _qpu_remote == None:
        _qpu_remote = ChimeraQPU(sites, couplers, cell_size, hardware_chimera_degree, site_range, coupler_range, chip_id=chip_id, endpoint=endpoint, solver_name=solver_name)
    return _qpu_remote


def build_cli_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--profile', help='connection details to load from dwave.conf', default=None)
    parser.add_argument('-ic', '--ignore-connection', help='force .dwrc connection details to be ignored', action='store_true', default=False)

    parser.add_argument('-tl', '--timeless', help='omit generation timestamp', action='store_true', default=False)
    parser.add_argument('-rs', '--seed', help='seed for the random number generator', type=int)
    parser.add_argument('-cd', '--chimera-degree', help='the size of a square chimera graph to utilize', type=int)
    parser.add_argument('-hcd', '--hardware-chimera-degree', help='the size of the square chimera graph on the hardware', type=int, default=16)
    parser.add_argument('-pp', '--pretty-print', help='pretty print json output', action='store_true', default=False)
    parser.add_argument('-os', '--omit-solution', help='omit any solutions produced by the problem generator', action='store_true', default=False)
    parser.add_argument('-iz', '--include-zeros', help='include zero values in output', action='store_true', default=False)
    parser.add_argument('-ccl', '--chimera-cell-limit', help='a limit the number of chimera cells used in the problem', type=int)

    parser.add_argument('-ccb', '--chimera-cell-box', help='two chimera cell coordinates define a box that is used to filter the hardware graph', nargs=4, type=int)


    subparsers = parser.add_subparsers()

    parser_const = subparsers.add_parser('const', help='generates a problem with constant coupling and/or field')
    parser_const.set_defaults(generator='const')
    parser_const.add_argument('-cp', '--coupling', help='set all couplers to the given value', type=float, default=0.0)
    parser_const.add_argument('-f', '--field', help='set all fields to the given value', type=float, default=0.0)
    parser_const.add_argument('-rgt', '--random-gauge-transformation', help='flip each spin by half chance using gauge transformation', action='store_true', default=False)

    parser_ran = subparsers.add_parser('ran', help='generates a random problem')
    parser_ran.set_defaults(generator='ran')
    parser_ran.add_argument('-pr', '--probability', help='the probability that a coupling or field agrees with the planted ground state', type=float, default=0.5)
    parser_ran.add_argument('-s', '--steps', help='the number of steps in random numbers', type=int, default=1)
    parser_ran.add_argument('-f', '--field', help='include a random field', action='store_true', default=False)
    parser_ran.add_argument('-sc', '--scale', help='scale feild and coupling values', type=float, default=1.0)
    parser_ran.add_argument('-sgs', '--simple-ground-state', help='makes the planted ground state be all spins -1', action='store_true', default=False)

    parser_gd = subparsers.add_parser('gd', help='generates a generic disordered problem from distribution parameters')
    parser_gd.set_defaults(generator='gd')
    parser_gd.add_argument('-cval', '--coupling-values', help='the candidate coupling values separated by spaces', type=float, default=[], nargs='*')
    parser_gd.add_argument('-cpr', '--coupling-probabilities', help='the probabilities of coupling values separated by spaces', type=float, default=[], nargs='*')
    parser_gd.add_argument('-fval', '--field-values', help='the candidate field values separated by spaces', type=float, default=[], nargs='*')
    parser_gd.add_argument('-fpr', '--field-probabilities', help='the probabilities of field values spaces', type=float, default=[], nargs='*')
    parser_gd.add_argument('-rgt', '--random-gauge-transformation', help='flip each spin by half chance using gauge transformation', action='store_true', default=False)

    parser_cbfm = subparsers.add_parser('cbfm', help='generates a corrupted biased ferromagnet problem')
    parser_cbfm.set_defaults(generator='cbfm')
    parser_cbfm.add_argument('-j1-val', help='the value of the first coupling', type=float, default=-1.0)
    parser_cbfm.add_argument('-j1-pr',  help='the probability of the first coupling', type=float, default=0.625)
    parser_cbfm.add_argument('-j2-val', help='the value of the second coupling', type=float, default=0.2)
    parser_cbfm.add_argument('-j2-pr',  help='the probability of the second coupling', type=float, default=0.375)
    parser_cbfm.add_argument('-h1-val', help='the value of the first field', type=float, default=-0.015)
    parser_cbfm.add_argument('-h1-pr',  help='the probability of the first field', type=float, default=0.625)
    parser_cbfm.add_argument('-h2-val', help='the value of the second field', type=float, default=0.015)
    parser_cbfm.add_argument('-h2-pr',  help='the probability of the second field', type=float, default=0.375)
    parser_cbfm.add_argument('-rgt', '--random-gauge-transformation', help='flip each spin by half chance using gauge transformation', action='store_true', default=False)

    parser_fl = subparsers.add_parser('fl', help='generates a frustrated loop problem')
    parser_fl.set_defaults(generator='fl')
    parser_fl.add_argument('-s', '--steps', help='the number of allowed steps in output Hamiltonian', type=int, default=2)
    parser_fl.add_argument('-a', '--alpha', help='site-to-loop ratio', type=float, default=0.2)
    parser_fl.add_argument('-mc', '--multicell', help='reject loops that are within one chimera cell', action='store_true', default=False)
    parser_fl.add_argument('-ccc', '--cluster-chimera-cells', help='treats each chimera cell as a single logical spin', action='store_true', default=False)
    parser_fl.add_argument('-sgs', '--simple-ground-state', help='makes the planted ground state be all spins -1', action='store_true', default=False)
    parser_fl.add_argument('-mll', '--min-loop-length', help='the minimum length of a loop', type=int, default=7)
    parser_fl.add_argument('-lrl', '--loop-reject-limit', help='the maximum amount of loops to be reject', type=int, default=1000)
    parser_fl.add_argument('-lsl', '--loop-sample-limit', help='the maximum amount of random walk samples', type=int, default=10000)

    parser_wscn = subparsers.add_parser('wscn', help='generates a weak-strong cluster network problem')
    parser_wscn.set_defaults(generator='wscn')
    parser_wscn.add_argument('-wf', '--weak-field', help='strength of the weak field', type=float, default=0.44)
    parser_wscn.add_argument('-sf', '--strong-field', help='strength of the strong field', type=float, default=-1)

    parser_fclg = subparsers.add_parser('fclg', help='generates a frustrated clustered loop and gadgets problem')
    parser_fclg.set_defaults(generator='fclg')
    parser_fclg.add_argument('-s', '--steps', help='the number of allowed steps in output Hamiltonian', type=int, default=3)
    parser_fclg.add_argument('-a', '--alpha', help='site-to-loop ratio', type=float, default=0.2)
    parser_fclg.add_argument('-gf', '--gadget-fraction', help='', type=float, default=0.1)
    parser_fclg.add_argument('-sgs', '--simple-ground-state', help='makes the planted ground state be all spins -1', action='store_true', default=False)
    parser_fclg.add_argument('-mll', '--min-loop-length', help='the minimum length of a loop', type=int, default=7)
    parser_fclg.add_argument('-lrl', '--loop-reject-limit', help='the maximum amount of loops to be reject', type=int, default=5000)
    parser_fclg.add_argument('-lsl', '--loop-sample-limit', help='the maximum amount of random walk samples', type=int, default=10000)

    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args())
