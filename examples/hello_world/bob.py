import asyncio
from asyncio import Future

from wsrpc import rpc, Service

service = Service("localhost", 6790)


@rpc(service)
async def print_message(message: str) -> None:
    print(f"Alice said: {message}")


async def main():
    await service.start()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
