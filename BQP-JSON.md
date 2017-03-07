# BQP-JSON

This document describes __bqp-json__, a json-based encoding for Binary Quadratic Programs (B-QP).  The formal specification is provided in the json-schema document, `bqp-schema.json`.  The goal of bqp-json is to provide a simple language-agnostic data standard for encoding B-QPs, to assist in research and development of B-QP solution methods.

Additionally, given the significant interest in using D-Wave's QPU for solving B-QP problems, bqp-json includes key features to assist in encoding D-Wave inspired test cases.

## Format Design Motivations

This section discusses some of the motivations for the design decisions of bqp-json.

### Spin vs Boolean Variables

In the operations research community, variables in B-QPs typically take boolean values (i.e. {0, 1}).  However, in the physics community the preference is for an ising interpretation where variables take spin values (i.e. {-1, 1}).  To readily support both of these formulations, bqp-json allows the problem variables to be defined as boolean or spin values.

### Solutions

A common approach when generating B-QPs is to _plant_ a predefined global optimal solution.  Knowledge of these planted solutions is useful when performing benchmarking experiments.  Hence, encoding of solutions is incorporated into the bqp-json format.

### Sparse Variable Identifiers

If a B-QP has _n_ decision variables, it is often convent to number those decision variables from 0 to n-1.  Indeed the qubits in a full yield D-Wave QPU are numbered from 0 to n-1.  In practice however, D-Wave QPUs have faults that eliminate some of the qubits.  To readily support the qubit identifiers of a D-Wave QPU, bqp-json adopts a sparse list of variable identifiers (e.g. {0, 1, 3, 7, ..., n-3, n-1}).

### Rescaling 

Due to the physical limits of analog hardware, it is often necessary to rescale a B-QP into the hardware's operating range.  bqp-json includes a _scaling_ parameter to retain the original units of the B-QP after the model parameters have been rescaled into the hardware's operating range.

### Metadata

When randomly generating B-QPs it is prudent to record some data about how the problem was generated.  For example, when generating a problem on a specific D-Wave QPU, it is helpful to be able to identify that QPU.  The bqp-json format includes a metadata block to record this type of information.


## The BQP-JSON Format

This section provides an informal and intuitive description of bqp-json.  Refer to `bqp-schema.json` for a formal specification.


### The Root Document

The root of a bqp-json document is as follows,
```
{
  "id": <integer>,
  "metadata": {...},
  "variable_ids": [...],
  "variable_domain": ("spin" | "boolean"),
  "scale": <float>,
  "offset": <float>,
  "linear_terms": [...],
  "quadratic_terms": [...],
  ("description": <string>,)
  ("solutions": [...])
}
```
Each of the top level items is as follows,
* _id_ - is an integer for identifying this bqp dataset
* _metadata_ - data describing how and when the problem was created
* _variable_ids_ - a list of integers defining the valid variable identifier values
* _variable_domain_ - indicates if the problem variables take boolean or spin values
* _scale_ - a scaling factor for the evaluation of the offset, linear and quadratic terms (typically 1.0)
* _offset_ - an offset for the evaluation of the linear and quadratic terms (typically 0.0)
* _linear_terms_ - a list of coefficients for individual variables (a.k.a. fields)
* _quadratic_terms_ - a list of coefficients for products variables (a.k.a. couplings)
* _description_ - an optional textual description of the bqp data 
* _solutions_ - an optional list of solution objects 


### Linear and Quadratic Terms

A linear term object has the form,
```
{
  "id": <integer>,
  "coeff": <float>
}
```
Where,
* _id_ - is the variable identifier value, it must appear in the "variable_ids" list
* _coeff_ - this is a floating point value defining the coefficient if the given variable

Each variable should be referenced no more than once in the "linear_terms" list.


A quadratic term object has the form,
```
{
  "id_tail": <integer>,
  "id_head": <integer>,
  "coeff": <float>
}
```
Where,
* _id_tail_ - is the first variable identifier value, it must appear in the "variable_ids" list
* _id_head_ - is the second variable identifier value, it must appear in the "variable_ids" list
* _coeff_ - this is a floating point value defining the coefficient of the product of the given variables

Each id pair should be referenced no more than once in the "quadratic_terms" list and the value of _id_tail_ cannot be the same as the value of _id_head_.  It is recommended, but not required, that _id_tail_ be less than _id_head_.

For example, this is __not__ allowed,
```
[
  {"id_tail": 0, "id_head": 1, "coeff": 2.4},
  {"id_tail": 0, "id_head": 1, "coeff": 1.7}
]
```
This is allowed, but not preferable,
```
[
  {"id_tail": 0, "id_head": 1, "coeff": 2.4},
  {"id_tail": 1, "id_head": 0, "coeff": 1.7}
]
```
This is the best practice,
```
[
  {"id_tail": 0, "id_head": 1, "coeff": 4.1}
]
```

### Solutions

A solution object has the form,
```
{
  "id": <integer>,
  "assignment": [...],
  ("description": <string>,)
  ("evaluation": <float>)
}
```
Where,
* _id_ - is an identifier of the solution
* _assignment_ - a list of assignment values for each variable defined in "variable_ids"
* _description_ - a textual description of what this solution is
* _evaluation_ - the evaluation of this solution in the given B-QP, to provided a correctness check

Each variable should be referenced exactly once in the "assignment" list.


An assignment object has the form,
```
{
  "id": <integer>,
  "value": <float>
}
```
Where,
* _id_ - is the variable identifier value, it must appear in the "variable_ids" list
* _value_ - this is the value given to that variable

If the "variable_domain" is "spin" the values should be either -1 or 1.
If the "variable_domain" is "boolean" the values should be either 0 or 1.


### Metadata
A solution object has the form,
```
{
  ("generated": <string>,)
  ("dwig_generator": <string>,)
  ("dw_url": <string>,)
  ("dw_solver_name": <string>,)
  ("dw_chip_id": <string>,)
  ("chimera_cell_size":  <integer>,)
  ("chimera_degree":  <integer>,)
  ...
}
```

Where,
* _generated_ - the utc time and date that the problem was generated
* _dwig_generator_ - the dwig algorithm used to generate the problem
* _dw_url_ - the url of the d-wave qpu used to generate the problem
* _dw_solver_name_ - the name of the d-wave solver used to generate the problem
* _dw_chip_id_ - the chip identifier of the d-wave qpu used to generate the problem
* _chimera_cell_size_ - the number of variables in each chimera unit cell
* _chimera_degree_ - the size of a square laytout of chimera unit cells

All of the metadata parameters are optional and arbitrary user defined parameters are permitted. 


