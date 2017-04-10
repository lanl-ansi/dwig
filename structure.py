import copy, random, math

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

    def build_dict(self):
        sorted_sites = sorted(self.spins.keys(), key=lambda x: x.index)

        assignment = [{'id':site.index, 'value':self.spins[site]} for site in sorted_sites]

        solution = {
            'id':self.identifier,
            'assignment':assignment,
            'evaluation':self.eval()
        }

        if self.description != None:
            solution['description'] = self.description

        data_dict = self.qpu_config.build_dict()
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

    def build_dict(self):
        sorted_sites = sorted(self.active_sites(), key=lambda x: x.index)

        quadratic_terms_data = []
        for (i,j) in sorted(self.couplings.keys(), key=lambda x:(x[0].index, x[1].index)):
            v = self.couplings[(i,j)]
            assert(v != 0)
            quadratic_terms_data.append({'id_tail':i.index, 'id_head':j.index, 'coeff':v})

        linear_terms_data = []
        for k in sorted(self.fields.keys(), key=lambda x: x.index):
            v = self.fields[k]
            assert(v != 0)
            linear_terms_data.append({'id':k.index, 'coeff':v})

        data_dict = {
            'version': bqpjson_version,
            'id': random.randint(0, 2**31 - 1),
            'variable_domain': 'spin',
            'variable_ids':[site.index for site in sorted_sites],
            'scale': self.scale,
            'offset': self.offset,
            'linear_terms':linear_terms_data,
            'quadratic_terms':quadratic_terms_data
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
    def __init__(self, sites, couplers, cell_size, chimera_degree, site_range, coupler_range, chimera_degree_view = None, chip_id = None):
        if chimera_degree_view == None:
            self.chimera_degree_view = chimera_degree
        else:
            self.chimera_degree_view = chimera_degree_view

        self.cell_size = int(cell_size)
        self.chip_id = chip_id

        self.sites = set([ChimeraSite(site, chimera_degree) for site in sites])

        site_lookup = { cn.index : cn for cn in self.sites }
        self.couplers = set([(site_lookup[i],site_lookup[j]) for i,j in couplers])
        self.chimera_degree = int(chimera_degree)
        self.site_range = site_range
        self.coupler_range = coupler_range


        self.chimera_cells = set()
        self.chimera_cell_sites = {}
        for site in self.sites:
            self.chimera_cells.add(site.chimera_cell)
            if site.chimera_cell not in self.chimera_cell_sites:
                self.chimera_cell_sites[site.chimera_cell] = set([])
            self.chimera_cell_sites[site.chimera_cell].add(site)
        #print(self.chimera_cell_sites)

        for i,j in couplers:
            assert(i in sites)
            assert(j in sites)

        for i,j in couplers:
            assert(i != j)

    def chimera_degree_filter(self, chimera_degree_view):
        assert(chimera_degree_view >= 1)

        filtered_sites = set([n.index for n in self.sites if n.is_chimera_degree(chimera_degree_view)])
        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, self.cell_size, self.chimera_degree, self.site_range, self.coupler_range, chimera_degree_view, self.chip_id)

    def cell_filter(self, max_cell):
        assert(max_cell >= 1)
        # TODO add warning if max_cell is larger than chimera_degree_view**2

        chimera_rows = max(s.chimera_row for s in self.sites)+1
        cell_distances = {}
        for s in self.sites:
            cell_distances[s.chimera_cell] = (s.chimera_cell_distance, s.chimera_row)

        cells = sorted(cell_distances, key=cell_distances.get)
        cells = set(cells[:max_cell])

        filtered_sites = set([n.index for n in self.sites if n.chimera_cell in cells])
        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, self.cell_size, self.chimera_degree, self.site_range, self.coupler_range, self.chimera_degree_view, self.chip_id)

    def chimera_cell(self, chimera_coordinate):
        return self.chimera_cell_coordinates(chimera_coordinate.row, chimera_coordinate.col)

    def chimera_cell_coordinates(self, chimera_row, chimera_column):
        assert(chimera_row > 0 and chimera_row <= self.chimera_degree_view)
        assert(chimera_column > 0 and chimera_column <= self.chimera_degree_view)

        return (chimera_row-1)*(self.chimera_degree) + (chimera_column-1)

    def __str__(self):
        return 'sites: '+\
            ' '.join([str(site) for site in self.sites])+'\ncouplers: '+\
            ' '.join(['('+str(i)+', '+str(j)+')' for i,j in self.couplers])


class ChimeraSite(object):
    def __init__(self, index, chimera_degree, unit_cell_size = 8):
        self.index = index
        self.chimera_cell = int(math.floor(index / unit_cell_size))
        self.chimera_row = int(math.floor(self.chimera_cell / chimera_degree))
        self.chimera_column = int(self.chimera_cell % chimera_degree)
        self.chimera_cell_distance = math.sqrt(self.chimera_row**2 + self.chimera_column**2)

    def is_chimera_degree(self, chimera_degree):
        return self.chimera_row+1 <= chimera_degree and self.chimera_column+1 <= chimera_degree

    def __str__(self):
        return str(self.index)

    # required so sorting works properly and problem generation is consistent
    def __lt__(self, other):
        return self.index < other.index
