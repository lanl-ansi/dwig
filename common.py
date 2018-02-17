import os, sys, json, bqpjson

class DWIGException(Exception):
    pass

# prints a line to standard error
def print_err(data):
    sys.stderr.write(str(data)+'\n')

json_dumps_kwargs = {
    'sort_keys':True,
    'indent':2,
    'separators':(',', ': ')
}

bqpjson_version = '1.0.0'

def validate_bqp_data(data):
    bqpjson.validate(data)
    return True


def get_chimera_adjacency(m, n, t):
    arcs = set([])
    for i in range(m):
        for j in range(n):
            offset = i*n*2*t + j*2*t
            for k in range(t):
                for l in range(t):
                    arcs.add((offset+k, offset+l+t))
                if i < m-1:
                    #print('a ', offset+k, offset+n*2*t)
                    arcs.add((offset+k, offset+k+n*2*t))
                if j < n-1:
                    #print('b ', offset+k+t, offset+k+t+2*t)
                    arcs.add((offset+k+t, offset+k+t+2*t))

    for i,j in [k for k in arcs]:
        arcs.add((j,i))

    return arcs
