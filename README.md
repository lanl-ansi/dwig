# D-Wave Instance Generator (D-WIG)

[![Build Status](https://travis-ci.org/lanl-ansi/dwig.svg?branch=master)](https://travis-ci.org/lanl-ansi/dwig) [![codecov](https://codecov.io/gh/lanl-ansi/dwig/branch/master/graph/badge.svg)](https://codecov.io/gh/lanl-ansi/dwig)

The D-WIG toolset is used to generate binary quadratic programs based on a specific D-Wave QPU.  A key motivation for generating problems on a specific QPU is that these problems do not require an embedding step to test them on the hardware.  The D-WIG problem generator assumes that the QPU has a chimera topology.

`dwig.py` is the primary entry point and generates binary unconstrained quadratic programming problems (B-QP) in the bqpjson format.

The remainder of this documentation assumes that,

1. You have access to a D-Wave QPU and the SAPI binaries
2. You are familiar with the D-Wave Qubist interface
3. You are using a bash terminal


## Installation

The D-WIG toolset requires `dwave-cloud-client`, `dwave_networkx` and `bqpjson` to run and `pytest` for testing.
These requirements can be installed with,
```
pip install -r requirements.txt
```

The installation can be tested by running,
```
./test.it
```

## Introduction

### Basic Usage

The primary entry point of the D-WIG toolset is `dwig.py` this script is used to generate a variety of B-QP problems, which have been studied in the literature.  For example, the following command will generate a RAN1 problem for a full yield QPU of chimera degree 12 and send it to standard output,
```
./dwig.py ran
```
Bash stream redirection can be used to save the standard output to a file, for example,
```
./dwig.py ran > ran1.json
```
The `ran1.json` file is a json document in the bqpjson format.  A detailed description of this format can be found in the [bqpjson](http://bqpjson.readthedocs.io/en/latest/bqpjson_format.html) python package.

A helpful feature of D-WIG is to reduce the size of the QPU that you are working with.  The _chimera degree_ argument `-cd n` can be used to reduce D-WIG's view of the full QPU to a smaller n-by-n QPU.  For example try,
```
./dwig.py -cd 2 ran
```
A detailed list of all command line options can be viewed via,
```
./dwig.py --help
```


### Problem Types

The D-Wig toolset currently supports three types of problem generation,

1. __const__ - fields are couplers are set to a given constant value
2. __ran__ - fields are couplers are set uniformly at random
3. __fl__ - frustrated loops
4. __wscn__ - weak-strong cluster networks
5. __fclg__ - frustrated cluster loops and gadgets

A detailed list of command line options for each problem type can be viewed via,
```
./dwig.py <problem type> --help
```
See the doc strings inside of `generator.py` for additional documentation on each of these problem types.


### Connecting to a QPU

D-WIG uses the `dwave-cloud-client` for connecting to the QPU and will use your `dwave.conf` file for the configuration details.  A specific profile can be selected with the command line argument `--profile <label>`.  If no configuration details are found, D-WIG will assume a full yield QPU of chimera degree 16.  The command line argument `--ignore-connection` can be used to ignore the defaults specified in `dwave.conf`. 


### Viewing a B-QP

The Qubist Solver Visualization tool is helpful in understanding complex B-QP datasets.  To that end, the `bqp2qh.py` script converts a B-QP problem into the Qubist Hamiltonian format so that it can be viewed in the Solver Visualization tool.  For example, the following command will generate a 2-by-2 RAN1 problem in the qubist format and then print it to standard output,
```
./dwig.py -cd 2 ran | bqp2qh
```
To view this problem paste the terminal output into the Data tab of the Qubist Solver Visualization tool.


### Spin vs Boolean Variables

The B-QP format supports problems with spin variables (i.e. {-1,1}) and boolean variables (i.e. {0,1}).  However, the D-WIG toolset generates problems only using spin variables.  The `spin2bool.py` tool can be used to make the transformation after the problem is generated.  For example, the following  command will generate 2-by-2 RAN1 problem and convert it to a boolean variable space,
```
./dwig.py -cd 1 ran | spin2bool -pp
```

### The QUBO Format

The QUBO format is supported by a variety of the tools provided by D-Wave, such as __qbsolv__, __aqc__, and __toq__.  The `bqp2qubo.py` tool can be combined with the `spin2bool.py` tool to convert D-WIG cases into the qubo format.  For example, the following  command will generate 2-by-2 RAN1 problem and convert it to the QUBO format,
```
./dwig.py -cd 1 ran | spin2bool | bqp2qubo
```

## Acknowledgments

This code has been developed as part of the Advanced Network Science Initiative at Los Alamos National Laboratory. The primary developer is Carleton Coffrin.

The D-WIG development team would like to thank Denny Dahl for suggesting the D-WIG name.  Special thanks are given to these works, which provided significant inspiration for the D-WIG toolset.

For the RAN-pr formulation,
```
@article{Zdeborova2016statistical,
  author = {Lenka Zdeborova and Florent Krzakala},
  title = {Statistical physics of inference: thresholds and algorithms},
  journal = {Advances in Physics},
  volume = {65},
  number = {5},
  pages = {453-552},
  year = {2016},
  doi = {10.1080/00018732.2016.1211393},
  URL = {http://dx.doi.org/10.1080/00018732.2016.1211393}
}
```

For the RAN-k formulation,
```
@article{king2015benchmarking,
  title={Benchmarking a quantum annealing processor with the time-to-target metric},
  author={King, James and Yarkoni, Sheir and Nevisi, Mayssam M and Hilton, Jeremy P and McGeoch, Catherine C},
  journal={arXiv preprint arXiv:1508.05087},
  year={2015}
}
```

For the FL-k formulation,
```
@article{king2015performance,
  title={Performance of a quantum annealer on range-limited constraint satisfaction problems},
  author={King, Andrew D and Lanting, Trevor and Harris, Richard},
  journal={arXiv preprint arXiv:1502.02098},
  year={2015}
}
```

For the FCL-k formulation,
```
@article{king2017quantum,
  title={Quantum Annealing amid Local Ruggedness and Global Frustration},
  author={King, James and Yarkoni, Sheir and Raymond, Jack and Ozfidan, Isil and King, Andrew D and Nevisi, Mayssam Mohammadi and Hilton, Jeremy P, and McGeoch, Catherine C},
  journal={arXiv preprint arXiv:1701.04579},
  year={2017}
}
```

For the weak-strong cluster network formulation,
```
@article{denchev2016computational,
  title={What is the Computational Value of Finite-Range Tunneling?},
  author={Denchev, Vasil S and Boixo, Sergio and Isakov, Sergei V and Ding, Nan and Babbush, Ryan and Smelyanskiy, Vadim and Martinis, John and Neven, Hartmut},
  journal={Physical Review X},
  volume={6},
  number={3},
  pages={031015},
  year={2016},
  publisher={APS}
}
```

For the frustrated cluster loops and gadgets formulation,
```
@article{albash2018advantage,
  title = {Demonstration of a Scaling Advantage for a Quantum Annealer over Simulated Annealing},
  author = {Albash, Tameem and Lidar, Daniel A.},
  journal = {Phys. Rev. X},
  volume = {8},
  issue = {3},
  pages = {031016},
  numpages = {26},
  year = {2018},
  month = {Jul},
  publisher = {American Physical Society},
  doi = {10.1103/PhysRevX.8.031016},
  url = {https://link.aps.org/doi/10.1103/PhysRevX.8.031016}
}
```

## License
D-WIG is provided under a BSD-ish license with a "modifications must be indicated" clause.  See the `LICENSE.md` file for the full text.
This package is part of the Hybrid Quantum-Classical Computing suite, known internally as LA-CC-16-032.
