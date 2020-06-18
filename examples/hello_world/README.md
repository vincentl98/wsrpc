# Hello World example

This example implements a basic one-way message sending 
service.

## How it works

- Bob starts up and wait for incoming calls
- Alice starts up
- Alice remotely calls `bob.print_message` and finishes
- Bob prints the message on his own `stdout`