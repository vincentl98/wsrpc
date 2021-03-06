import asyncio
from asyncio import Future

from wsrpc import rpc, Service


class BobService(Service):

    def __init__(self):
        super().__init__("localhost", 6788)
        self.alice_value = Future()
        self.stephanie_value = Future()

    @rpc
    async def set_alice_value(self, value: int) -> None:
        print(f"Received Alice value: {value}")
        self.alice_value.set_result(value)

    @rpc
    async def set_stephanie_value(self, value: int) -> None:
        print(f"Received Stephanie value: {value}")
        self.stephanie_value.set_result(value)

    async def value(self):
        return await self.alice_value + await self.stephanie_value


async def main():
    service = BobService()
    await service.start()
    print(f"Multiplication result: {await service.value()}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
