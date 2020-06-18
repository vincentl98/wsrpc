# secured_call

This example implements a one-way message sending 
service with token authentication and SSL.

SSL authentication is automatically enabled when passing 
`ssl_certificate_filename` to `Service` constructor. 

## How to generate a self-signed certificate

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.pem -out localhost.pem`

When prompted: `Common Name (e.g. server FQDN or YOUR name):`,
type `localhost`.

## How it works

Note: In this example, Bob is the trusted party, and
Alice wants to be authenticated.

- Alice starts up
- Bob starts up
- Alice tries to send a message without her token
- Bob denies her request
- Alice tries to send a message with her token
- Bob accepts her request