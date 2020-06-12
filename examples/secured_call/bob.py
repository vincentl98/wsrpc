import asyncio
from asyncio import Future

from wsrpc.decorators import rpc
from wsrpc.service import Service

service = Service("localhost", 6790,
                  ssl_certificate_filename="localhost.pem")


class InvalidTokenError(Exception):
    pass

exports = [InvalidTokenError]

trusted_tokens = ["alice_token_123"]  # This is just an illustration. Tokens should never be stored in code.


@rpc(service)
async def print_message(message: str, token: str = None) -> None:
    if token is None or token not in trusted_tokens:
        raise InvalidTokenError()
    else:
        print(f"Alice said: {message}")


async def main():
    await service.start()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
