import asyncio
from asyncio import Future

from wsrpc.decorators import class_rpc
from wsrpc.state_service import StateService


class HelloService(StateService):

    @class_rpc
    async def hello(self) -> str:
        return "Hello World!"


service = HelloService("localhost", 5678)


async def main():
    await service.start()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
