import asyncio
import tensorflow as tf
from asyncio import Future

from wsrpc import rpc, StatelessService

service = StatelessService("localhost", 6790,
                           ssl_certificate_filename="localhost.pem")

trusted_tokens = ["alice_token_123"]  # This is just an illustration. Tokens should never be stored in code.


@rpc(service)
async def print_message(message: tf.Tensor, token: str = None) -> None:
    if token is None or token not in trusted_tokens:
        from examples.secured_call.exceptions import InvalidTokenError
        raise InvalidTokenError()
    else:
        print(f"Alice said: {message}")


async def main():
    await service.start()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
