# MPC Matrix Multiplication

This example implements matrix multiplication of two matrices. Alice owns A, Stéphanie ows B, and Bob receives: `A*B`, where `*` denotes matrix product.

## Running

The `wsrpc` package should be added to `PYTHONPATH`.
Alternatively, you can move the Python files of this example
at the root of the project, and manually fix dependencies. 


## How it works

It is a generalization of MPC multiplication. See [explanations](https://medium.com/dropoutlabs/secret-sharing-explained-acf092660d97) on Medium by Dropout Labs for more information on MPC multiplication.