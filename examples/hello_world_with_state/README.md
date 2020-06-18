# Hello World with state

This example implements a basic one-way message sending 
service holding the count of received messages.

## How it works

- Bob starts up and wait for incoming calls
- Alice starts up
- Alice remotely calls `bob.print_message` three times
- Bob prints the message and the message count on his own `stdout`