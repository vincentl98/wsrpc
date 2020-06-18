# hello_world

This example implements a basic one-way message sending 
service.

## Running

The `wsrpc` package should be added to `PYTHONPATH`.
Alternatively, you can move the Python files of this example
at the root of the project, and manually fix dependencies. 

## How it works

- Bob starts up and wait for incoming calls
- Alice starts up
- Alice remotely calls `bob.print_message` and finishes
- Bob prints the message on his own `stdout`