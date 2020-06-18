# hello_world_class

This example implements a basic one-way message sending 
service with a `ServiceState` object.

## Running

The `wsrpc` package should be added to `PYTHONPATH`.
Alternatively, you can move the Python files of this example
at the root of the project, and manually fix dependencies. 

## How it works

- Bob starts up and wait for incoming calls
- Alice starts up
- Alice remotely calls `bob.print_message` three times
- Bob prints the message and the message count on his own `stdout`