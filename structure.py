import copy, math


class QPUConfiguration(object):
    def __init__(self, qpu, fields={}, couplings={}):
        self.qpu = qpu
        self.fields = fields
        self.couplings = couplings

        for k, v in fields.items():
            assert(qpu.site_range[0] <= v and qpu.site_range[1] >= v)
            assert(k in qpu.sites)

        for k, v in couplings.items():
            assert(qpu.coupler_range[0] <= v and qpu.coupler_range[1] >= v)
            assert(k in qpu.couplers)

    def qubist_hamiltonian(self):
        lines = []
        lines.append('%d %d' % (max([site.index for site in self.qpu.sites]), len(self.fields) + len(self.couplings)))
        for i, v in self.fields.items():
            lines.append('%d %d %f' % (i.index, i.index, v))
        for (i ,j), v in self.couplings.items():
            lines.append('%d %d %f' % (i.index, j.index, v))
        return '\n'.join(lines)

    def __str__(self):
        return 'fields: '+\
            ' '.join([str(site)+':'+str(value) for site, value in self.fields.items()]) +\
            '\ncouplings: '+' '.join(['('+str(i)+', '+str(j)+'):'+str(value) for (i,j), value in self.couplings.items()])


class ChimeraQPU(object):
    def __init__(self, sites, couplers, chimera_degree, site_range, coupler_range):
        self.sites = set([ChimeraSite(site, chimera_degree) for site in sites])

        site_lookup = { cn.index : cn for cn in self.sites }
        self.couplers = set([(site_lookup[i],site_lookup[j]) for i,j in couplers])
        self.chimera_degree = chimera_degree
        self.site_range = site_range
        self.coupler_range = coupler_range

    def chimera_degree_filter(self, chimera_degree):
        assert(chimera_degree >= 1)

        filtered_sites = set([n.index for n in self.sites if n.is_chimera_degree(chimera_degree)])
        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, chimera_degree, self.site_range, self.coupler_range)

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

    def is_chimera_degree(self, chimera_degree):
        return self.chimera_row+1 <= chimera_degree and self.chimera_column+1 <= chimera_degree

    def __str__(self):
        return str(self.index)
