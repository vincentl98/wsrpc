# mpc_sum

This example implements a secret sum using a random
generated value `r`.

## Running

The `wsrpc` package should be added to `PYTHONPATH`.
Alternatively, you can move the Python files of this example
at the root of the project, and manually fix dependencies. 


## How it works

- Stephanie starts up first
- Alice starts up second
- Alice calls Stephanie to set `r` value: `set_r` function
- Bob starts up last
- Bob calls Alice and Stephanie to get their
encrypted values: `await alice.encrypted_value()`

Note: to keep `r` secret, Alice calls Stephanie to
set her `r` value, and not the other way around. 
We could have another approach by defining a
`get_r` function to Alice, but then Bob would 
have access to `r`.