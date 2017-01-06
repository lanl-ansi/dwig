import copy, math

class QPUConfiguration(object):
    def __init__(qpu, field, coupling):
        pass


class ChimeraQPU(object):
    def __init__(self, sites, couplers, chimera_degree, site_range = (-2.0, 2.0), coupler_range = (-1.0, 1.0)):
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

        return ChimeraQPU(filtered_sites, filtered_couplers, chimera_degree)

    def __str__(self):
        return 'sites: '+str(self.sites)+'\ncouplers: '+str(self.couplers)


class ChimeraSite(object):
    def __init__(self, index, chimera_degree):
        self.index = index
        self.chimera_cell = int(math.floor(index / 8))
        self.chimera_row = int(math.floor(self.chimera_cell / chimera_degree))
        self.chimera_column = int(self.chimera_cell % chimera_degree)

    def is_chimera_degree(self, chimera_degree):
        return self.chimera_row+1 <= chimera_degree and self.chimera_column+1 <= chimera_degree

    def __str__(self):
        return 's_'+str(self.index)
