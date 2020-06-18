import asyncio
from asyncio import Future

from wsrpc import Service, rpc

service = Service("localhost", 6788)


@rpc(service)
async def set_alice_value(value: int) -> None:
    print(f"Received Alice value: {value}")
    alice_value.set_result(value)


@rpc(service)
async def set_stephanie_value(value: int) -> None:
    print(f"Received Stephanie value: {value}")
    stephanie_value.set_result(value)


async def main():
    global alice_value, stephanie_value
    alice_value = Future()
    stephanie_value = Future()

    await service.start()
    await alice_value
    await stephanie_value
    print(f"Multiplication result: {await alice_value + await stephanie_value}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
