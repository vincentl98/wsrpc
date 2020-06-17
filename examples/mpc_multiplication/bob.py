import asyncio
from asyncio import Future

from wsrpc import Service, rpc

service = Service("localhost", 6788)

if __name__ == "__main__":
    alice_value = Future()
    stephanie_value = Future()


@rpc(service)
async def set_alice_value(value: int) -> None:
    global alice_value
    print("received alice value")
    alice_value.set_result(value)


@rpc(service)
async def set_stephanie_value(value: int) -> None:
    global stephanie_value
    print("received stephanie value")
    stephanie_value.set_result(value)


async def main():
    await service.start()
    await alice_value
    await stephanie_value
    print(f"{await alice_value} + {await stephanie_value} = {await alice_value + await stephanie_value}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
