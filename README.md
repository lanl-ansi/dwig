# D-Wave Instance Generator (D-WIG)

This script is used to generate interesting binary quadratic programs, which are compatible with a specific D-Wave QPU.  It assumes the QPU has a chimera topology.

This code includes,
* bqp-schema.json - a JSON-Schema for encoding B-QP optimization problems
* dwig.py - a tool for generating B-QP problems in the bqp-json format
* spin2bool.py - a tool for converting a bqp-json from ising variables to boolean variables and back
* bqp2qh.py - a tool for converting a bqp-json file into a qubist hamiltonian


### Simple Tests

```
./dwig.py -cd 1 ran
./dwig.py -cd 1 ran | ./bqp2qh.py
./dwig.py -cd 1 ran | ./spin2bool.py
./dwig.py -cd 2 fl | ./bqp2qh.py
./dwig.py -cd 6 wscn | ./bqp2qh.py
```
