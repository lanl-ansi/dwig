import copy, random, math
import dwave_networkx as dnx

from collections import namedtuple

from common import print_err
from common import bqpjson_version

class QPUAssignment(object):
    def __init__(self, qpu_config, spins={}, identifier=0, description=None):
        self.qpu_config = qpu_config
        self.spins = spins
        self.identifier = identifier
        self.description = description

        for k, v in self.spins.items():
            assert(k in self.qpu_config.qpu.sites)
            assert(v == -1 or v == 1)

        active_sites = self.qpu_config.active_sites()
        assert(len(self.spins) == len(active_sites))
        for site in active_sites:
            assert(site in spins.keys())

    def eval(self):
        energy = sum([field*self.spins[site] for site, field in self.qpu_config.fields.items()])
        #print(energy)
        for coupler, coupling in self.qpu_config.couplings.items():
            energy += coupling*self.spins[coupler[0]]*self.spins[coupler[1]]
            #print(coupling*self.spins[coupler[0]]*self.spins[coupler[1]])
        return self.qpu_config.scale*(energy + self.qpu_config.offset)

    def build_dict(self, zeros=False):
        sorted_sites = sorted(self.spins.keys(), key=lambda x: x.index)

        assignment = [{'id':site.index, 'value':self.spins[site]} for site in sorted_sites]

        solution = {
            'id':self.identifier,
            'assignment':assignment,
            'evaluation':self.eval()
        }

        if self.description != None:
            solution['description'] = self.description

        data_dict = self.qpu_config.build_dict(zeros)
        data_dict['solutions'] = [solution]

        return data_dict

    def __str__(self):
        return 'spins: '+\
            ' '.join([str(site)+':'+str(value) for site, value in self.spins.items()])


class QPUConfiguration(object):
    def __init__(self, qpu, fields={}, couplings={}, offset=0.0, unitless=True):
        scaled_fields, scaled_couplings, scaled_offset, scale = _rescale(fields, couplings, offset, qpu.site_range, qpu.coupler_range)

        filtered_fields = {k:v for k,v in scaled_fields.items() if v != 0.0}
        filtered_couplings = {k:v for k,v in scaled_couplings.items() if v != 0.0}

        self.qpu = qpu
        self.fields = filtered_fields
        self.couplings = filtered_couplings
        self.offset = scaled_offset
        self.scale = 1.0
        if not unitless:
            self.scale = scale

        for k, v in self.fields.items():
            assert(qpu.site_range.lb <= v and qpu.site_range.ub >= v)
            assert(k in qpu.sites)

        for k, v in self.couplings.items():
            assert(qpu.coupler_range.lb <= v and qpu.coupler_range.ub >= v)
            assert(k in qpu.couplers)

    def active_sites(self):
        active = set(self.fields.keys())
        active |= set([key[0] for key in self.couplings.keys()])
        active |= set([key[1] for key in self.couplings.keys()])
        return active

    def build_dict(self, zeros=False):
        sorted_sites = sorted(self.active_sites(), key=lambda x: x.index)

        quadratic_terms_data = []
        for (i,j) in sorted(self.couplings.keys(), key=lambda x:(x[0].index, x[1].index)):
            v = self.couplings[(i,j)]
            if not zeros:
                assert(v != 0)
            quadratic_terms_data.append({'id_tail':i.index, 'id_head':j.index, 'coeff':v})

        linear_terms_data = []
        for k in sorted(self.fields.keys(), key=lambda x: x.index):
            v = self.fields[k]
            if not zeros:
                assert(v != 0)
            linear_terms_data.append({'id':k.index, 'coeff':v})

        data_dict = {
            'version': bqpjson_version,
            'id': random.randint(0, 2**31 - 1),
            'variable_domain': 'spin',
            'variable_ids': [site.index for site in sorted_sites],
            'scale': self.scale,
            'offset': self.offset,
            'linear_terms': linear_terms_data,
            'quadratic_terms': quadratic_terms_data
        }

        return data_dict

    def __str__(self):
        return 'fields: '+\
            ' '.join([str(site)+':'+str(value) for site, value in self.fields.items()]) +\
            '\ncouplings: '+' '.join(['('+str(i)+', '+str(j)+'):'+str(value) for (i,j), value in self.couplings.items()])


def _rescale(fields, couplings, offset, site_range, coupler_range):
    assert(site_range.lb + site_range.ub == 0.0)
    assert(coupler_range.lb + coupler_range.ub == 0.0)

    scaling_factor = 1.0
    scale = 1.0

    for field in fields.values():
        if field != 0:
            if field < site_range.lb:
                scaling_factor = min(scaling_factor, site_range.lb/float(field))
            if field > site_range.ub:
                scaling_factor = min(scaling_factor, site_range.ub/float(field))

    for coupling in couplings.values():
        if coupling != 0:
            if coupling < coupler_range.lb:
                scaling_factor = min(scaling_factor, coupler_range.lb/float(coupling))
            if coupling > coupler_range.ub:
                scaling_factor = min(scaling_factor, coupler_range.ub/float(coupling))

    if scaling_factor < 1.0:
        print_err('info: rescaling field to {} and couplings to {} with scaling factor {}'.format(site_range, coupler_range, scaling_factor))
        fields = {k:v*scaling_factor for k,v in fields.items()}
        couplings = {k:v*scaling_factor for k,v in couplings.items()}
        offset = offset*scaling_factor
        scale = 1/scaling_factor

    return fields, couplings, offset, scale


ChimeraCoordinate = namedtuple('ChimeraCordinate', ['row', 'col'])
Range = namedtuple('Range', ['lb', 'ub'])


class ChimeraQPU(object):
    def __init__(self, sites, couplers, cell_size, chimera_degree, site_range, coupler_range, chimera_degree_view = None, chip_id = None, endpoint = None, solver_name = None):
        if chimera_degree_view == None:
            self.chimera_degree_view = chimera_degree
        else:
            self.chimera_degree_view = chimera_degree_view

        # This should be unique to the architecture.
        self.cell_size = int(cell_size)

        # This identifier is returned by the annealer.
        self.chip_id = chip_id

        # Endpoint URL to the solver and its name.
        self.endpoint = endpoint
        self.solver_name = solver_name

        # These are all the possible sites, i.e., each site is a qubit.
        self.sites = set([ChimeraSite(site, chimera_degree) for site in sites])

        # Integers associated with each qubit: lookup from qubit integer to site object.
        site_lookup = { cn.index : cn for cn in self.sites }

        # Map all of the qubit chimera site object pairs (i.e., couplers).
        self.couplers = set([(site_lookup[i],site_lookup[j]) for i,j in couplers])
        self.chimera_degree = int(chimera_degree)

        # A tuple (0, max_site_id) describing the range of site indices.
        self.site_range = site_range

        # A tuple (0, max_coupler_id) describing the range of coupler indices.
        # The max index should always be the length of the coupler list.
        self.coupler_range = coupler_range

        self.chimera_cells = set()
        self.chimera_cell_sites = {}

        for site in self.sites:
            # Tries to add all unique chimera cell indices.
            self.chimera_cells.add(site.chimera_cell)

            if site.chimera_cell not in self.chimera_cell_sites:
                self.chimera_cell_sites[site.chimera_cell] = set([])

            # Add qubit/site to the corresponding chimera cell.
            self.chimera_cell_sites[site.chimera_cell].add(site)

        for i,j in couplers:
            assert(i in sites)
            assert(j in sites)

        for i,j in couplers:
            assert(i != j)

    def chimera_degree_filter(self, chimera_degree_view):
        assert(chimera_degree_view >= 1)

        # is_chimera_degree says if a qubit is within a chimera graph of a certain degree.
        filtered_sites = set([n.index for n in self.sites if n.is_chimera_degree(chimera_degree_view)])

        # Filter all the couplers that apply to the qubits from above.
        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, self.cell_size, self.chimera_degree, self.site_range, self.coupler_range, chimera_degree_view, self.chip_id, self.endpoint, self.solver_name)

    # Try to fill in the chimera subgraph diagonally.
    def cell_filter(self, max_cell):
        assert(max_cell >= 1)
        # TODO: Add warning if `max_cell` is larger than `chimera_degree_view**2`.

        # Chimera row indices start from zero. This is the number of rows below zero.
        chimera_rows = max(s.chimera_row for s in self.sites) + 1

        cell_distances = {}
        for s in self.sites:
            # Euclidean distance of cell from upper left (?)
            cell_distances[s.chimera_cell] = (s.chimera_cell_distance, s.chimera_row)

        cells = sorted(cell_distances, key=cell_distances.get)
        cells = set(cells[:max_cell])

        filtered_sites = set([n.index for n in self.sites if n.chimera_cell in cells])
        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, self.cell_size, self.chimera_degree, self.site_range, self.coupler_range, self.chimera_degree_view, self.chip_id, self.endpoint, self.solver_name)

    # Allows you to define the box, even within the middle of the graph. The
    # arguments are cells that define the upper part and lower parts.
    def chimera_cell_box_filter(self, chimera_cell_1, chimera_cell_2):
        # Starting and ending rows and columns in the box.
        chimera_rows = (chimera_cell_1[0], chimera_cell_2[0])
        chimera_columns = (chimera_cell_1[1], chimera_cell_2[1])

        # Checks to make sure the box that's been specified is valid
        assert(chimera_rows[0] >= 0 and chimera_rows[0] <= self.chimera_degree_view)
        assert(chimera_rows[1] >= 0 and chimera_rows[1] <= self.chimera_degree_view)
        assert(chimera_rows[0] <= chimera_rows[1])
        assert(chimera_columns[0] >= 0 and chimera_columns[0] <= self.chimera_degree_view)
        assert(chimera_columns[1] >= 0 and chimera_columns[1] <= self.chimera_degree_view)
        assert(chimera_columns[0] <= chimera_columns[1])

        # Filter all qubits and couplers that reside within the box, only.
        filtered_sites = set([])
        for site in self.sites:
            if site.chimera_row >= chimera_rows[0] and site.chimera_row <= chimera_rows[1] and \
                site.chimera_column >= chimera_columns[0] and site.chimera_column <= chimera_columns[1]:
                filtered_sites.add(site.index)

        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, self.cell_size, self.chimera_degree, self.site_range, self.coupler_range, self.chimera_degree_view, self.chip_id, self.endpoint, self.solver_name)

    def spin_filter(self, spin_set):
        # Collection of integer indices.
        spin_set = set(spin_set)

        filtered_sites = set([])
        for site in self.sites:
            if site.index in spin_set:
                filtered_sites.add(site.index)

        filtered_couplers = []
        for i,j in self.couplers:
            if (i.index in filtered_sites and j.index in filtered_sites):
                coupler = (i.index,j.index)
                filtered_couplers.append(coupler)

        return ChimeraQPU(filtered_sites, filtered_couplers, self.cell_size, self.chimera_degree, self.site_range, self.coupler_range, self.chimera_degree_view, self.chip_id, self.endpoint, self.solver_name)

    def coupler_filter(self, coupler_set):
        # coupler_set is a vector of integer tuples
        # coupler_sites is the vector of coupler objects
        coupler_sites = set([])
        for (i,j) in coupler_set:
            coupler_sites.add(i)
            coupler_sites.add(j)

        filtered_sites = set([])
        for site in self.sites:
            if site.index in coupler_sites:
                filtered_sites.add(site.index)

        filtered_couplers = []
        for i,j in self.couplers:
            if (i.index in filtered_sites and j.index in filtered_sites):
                coupler = (i.index, j.index)
                if coupler in coupler_set:
                    filtered_couplers.append(coupler)

        # Check if one of the couplers doesn't exist in the hardware and error out, if so.
        if len(filtered_couplers) != len(coupler_sites):
            print_err('warning: given a coupler set of size {} but found only {} active couplings from this set'.format(len(coupler_sites), len(filtered_couplers)))
            filtered_sites = set([])
            for (i,j) in filtered_couplers:
                filtered_sites.add(i)
                filtered_sites.add(j)

        return ChimeraQPU(filtered_sites, filtered_couplers, self.cell_size, self.chimera_degree, self.site_range, self.coupler_range, self.chimera_degree_view, self.chip_id, self.endpoint, self.solver_name)


    def chimera_cell(self, chimera_coordinate):
        return self.chimera_cell_coordinates(chimera_coordinate.row, chimera_coordinate.col)

    def chimera_cell_coordinates(self, chimera_row, chimera_column):
        assert(chimera_row > 0 and chimera_row <= self.chimera_degree_view)
        assert(chimera_column > 0 and chimera_column <= self.chimera_degree_view)

        # Flattened index of the chimera cell.
        return (chimera_row-1)*(self.chimera_degree) + (chimera_column-1)

    def __str__(self):
        return 'sites: '+\
            ' '.join([str(site) for site in self.sites])+'\ncouplers: '+\
            ' '.join(['('+str(i)+', '+str(j)+')' for i,j in self.couplers])


# Class for an individual qubit in a Chimera graph.
class ChimeraSite(object):
    def __init__(self, index, chimera_degree, unit_cell_size = 8):
        # Derive associated cell information from the qubit data alone.
        self.index = index

        # We need to know the numbering convention of the Chimera layout to derive the below.
        self.chimera_cell = self.index//unit_cell_size
        self.chimera_cell_row = (self.index%unit_cell_size)//(unit_cell_size/2)
        self.chimera_row = self.chimera_cell//chimera_degree
        self.chimera_column = self.chimera_cell%chimera_degree
        self.chimera_cell_distance = math.sqrt(self.chimera_row**2 + self.chimera_column**2)

    def is_chimera_degree(self, chimera_degree):
        return self.chimera_row+1 <= chimera_degree and self.chimera_column+1 <= chimera_degree

    def __str__(self):
        return str(self.index)

    # required so sorting works properly and problem generation is consistent
    def __lt__(self, other):
        return self.index < other.index

class PegasusSite(object):
    def __init__(self, index):
        # Index of the qubit.
        self.index = index

    # "String" definition for naming the Pegasus site.
    def __str__(self):
        return str(self.index)

    # "Less than" definition, later required for problem generation.
    def __lt__(self, other):
        return self.index < other.index


class PegasusQPU(object):
    def __init__(
        self, sites, couplers, site_range, coupler_range,
        chip_id = None, endpoint = None, solver_name = None):
        # Cell size, unique to the Pegasus architecture.
        #self.cell_size = 24

        # Initialize the set of all possible sites.
        self.sites = set([PegasusSite(site_index) for site_index in sites])

        # Map site indices to site objects via the `site_lookup` dictionary.
        site_lookup = {site.index : site for site in self.sites}

        # Define the set of couplers with respect to the site objects.
        self.couplers = set([(site_lookup[i], site_lookup[j]) for i, j in couplers])

        # Tuple that stores the minimum and maximum site indices.
        self.site_range = site_range

        # Tuple that stores the minimum and maximum coupler indices.
        self.coupler_range = coupler_range

        for i, j in couplers:
            # Coupler indices should appear in sites.
            assert(i in sites)
            assert(j in sites)

        for i, j in couplers:
            # A qubit can't be coupled to itself.
            assert(i != j)

        # This is specific to the D-Wave solver being used.
        self.chip_id = chip_id

        # URL of the solver endpoint.
        self.endpoint = endpoint

        # Name of the solver corresponding to the endpoint.
        self.solver_name = solver_name

    def pegasus_lattice_size_filter(self, pegasus_lattice_size):
        # Ensure the Pegasus lattice size is valid.
        assert(pegasus_lattice_size >= 2)

        # Get flattened indices of the expected Pegasus subgraph.
        pegasus_coordinates = dnx.pegasus_coordinates(16) # Specific for the Advantage.
        graph = dnx.pegasus_graph(pegasus_lattice_size, nice_coordinates = True) # Subgraph size.
        linear_indices = [pegasus_coordinates.nice_to_linear(x) for x in list(graph.nodes)]

        # Get the index set of all nodes.
        linear_node_set = set(linear_indices)
        qpu_site_indices = set([x.index for x in self.sites])
        filtered_sites = linear_node_set.intersection(qpu_site_indices)

        # Filter couplers to include only the sites from above.
        filtered_couplers = [(i.index, j.index) for i, j in self.couplers if \
            (i.index in filtered_sites and j.index in filtered_sites)]

        return PegasusQPU(
            filtered_sites, filtered_couplers, self.site_range,
            self.coupler_range, self.chip_id, self.endpoint, self.solver_name)
