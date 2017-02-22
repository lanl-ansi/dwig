# BQP-JSON

This document describes __bqp-json__, a json-based encoding for Binary Quadratic Programs (B-QP).  The formal specification is provided in the json-schema document, `bqp-schema.json`.  The goal of bqp-json is to provide a simple language-agnostic data standard for encoding B-QPs, to assist in research and development of B-QP solution methods.

Additionally, given the significant interest in using D-Wave's QPU for solving B-QP problems, bqp-json includes key features to assist in encoding D-Wave inspired test cases.

## Format Design Motivations

This section discusses some of the motivations for the design decisions of bqp-json.

### Spin vs Boolean Variables

In the operations research community, variables in B-QPs typically take boolean values (i.e. {0, 1}).  However, in the physics community the preference is for an ising interpretation where variables take spin values (i.e. {-1, 1}).  To readily support both of these formulations, bqp-json allows the problem variables to be defined as boolean or spin values.

### Solutions

A common approach when generating B-QPs is to _plant_ a predefined global optimal solution.  Knowledge of these planted solutions is useful when performing benchmarking experiments.  Hence, encoding of solutions is incorporated into the bqp-json format.

### Sparse Variable Indexes 

If a B-QP has _n_ decision variables, it is often convent to number those decision variables from 0 to n-1.  Indeed the qubits in a full yield D-Wave QPU are numbered from 0 to n-1.  In practice however, D-Wave QPUs have faults that eliminate some of the qubits.  To readily support the qubit incidences of a D-Wave QPU, bqp-json adopts a sparse list of variable incidences (e.g. {0, 1, 3, 7, ..., n-3, n-1}).

### Metadata

When randomly generating B-QPs it is prudent to record some data about how the problem was generated.  For example, when generating a problem on a specific D-Wave QPU, it is helpful to be able to identify that QPU.  The bqp-json format includes a metadata block to record this type of information.


## The BQP-JSON Format

This section provides an informal and intuitive description of bqp-json.  Refer to `bqp-schema.json` for a formal specification.


### The Root Document

The root of a bqp-json document is as follows,
```
{
  "metadata": {...},
  "variable_idxs": [...],
  "variable_domain": ("spin" | "boolean"),
  "offset": <float>,
  "linear_terms": [...],
  "quadratic_terms": [...],
  ("solutions": [...])
}
```
Each of the top level items is as follows,
* _metadata_ - data describing how and when the problem was created.
* _variable_idxs_ - a list of integers defining the valid variable index values
* _variable_domain_ - indicates if the problem variables take boolean or spin values
* _offset_ - an offset for the evaluation of the linear and quadratic terms
* _linear_terms_ - a list of coefficients for individual variables (a.k.a. fields)
* _quadratic_terms_ - a list of coefficients for products variables (a.k.a. couplings)
* _solutions_ - a list of solution objects 


### Linear and Quadratic Terms

A linear term object has the form,
```
{
  "idx": <integer>,
  "coeff": <float>
}
```
Where,
* _idx_ - is the variable index value, it must appear in the "variable_idxs" list
* _coeff_ - this is a floating point value defining the coefficient if the given variable

Each variable should not be referenced more than once in the "linear_terms" list.


A quadratic term object has the form,
```
{
  "idx_1": <integer>,
  "idx_2": <integer>,
  "coeff": <float>
}
```
Where,
* _idx_1_ - is the first variable index value, it must appear in the "variable_idxs" list
* _idx_2_ - is the second variable index value, it must appear in the "variable_idxs" list
* _coeff_ - this is a floating point value defining the coefficient of the product of the given variables

By convention idx_1 should be strictly less than idx_2.  Each variable pair should not be referenced more than once in the "quadratic_terms" list.


### Solutions

A solution object has the form,
```
{
  "idx": <integer>,
  "assignment": [...],
  "description": <string>,
  ("evaluation": <float>)
}
```
Where,
* _idx_ - is an identifier of the solution
* _assignment_ - a list of assignment values for each variable defined in "variable_idxs"
* _description_ - a textual description of what this solution is
* _evaluation_ - the evaluation of this solution in the given B-QP, to provided a correctness check

Each variable should not be referenced exactly once in the "assignment" list.


An assignment object has the form,
```
{
  "idx": <integer>,
  "value": <float>
}
```
Where,
* _idx_ - is the variable index value, it must appear in the "variable_idxs" list
* _value_ - this is the value given to that variable

If the "variable_domain" is "spin" the values should be either -1 or 1.
If the "variable_domain" is "boolean" the values should be either 0 or 1.


### Metadata
A solution object has the form,
```
{
  ("generated": <string>),
  ("generator": <string>),
  ("dw_url": <string>),
  ("dw_solver_name": <string>),
  ("dw_chip_id": <string>),
  ...
}
```
Where,
* _generated_ - the utc time and date that the problem was generated
* _generator_ - the algorithm used to generate the problem
* _dw_url_ - the url of the d-wave qpu used to generate the problem
* _dw_solver_name_ - the name of the d-wave solver used to generate the problem
* _dw_chip_id_ - the chip identifier of the d-wave qpu used to generate the problem

All of the metadata parameters are optional and arability user defined parameters are permitted. 


