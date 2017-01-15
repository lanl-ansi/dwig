# dwpg - D-Wave Problem Generator

This script is used to randomly generate interesting binary quadratic programs that are compatible with a target D-Wave QPU.  It assumes the QPU has a chimera topology.

This code includes two tools,
* dwpg.py - for generating B-QP problems in the bqp-json format
* bqp2qh.py - takes a bqp-json file and prints a qubist hamiltonian

### Simple Tests

`./dwpg.py -cd 1 ran`
`./dwpg.py -cd 1 ran | ./bqp2qh.py`
