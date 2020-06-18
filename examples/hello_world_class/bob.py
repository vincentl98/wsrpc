import asyncio
from asyncio import Future

from wsrpc.decorators import class_rpc
from wsrpc.state_service import StateService


class BobService(StateService):

    def init_state(self) -> None:
        self.messages_count = 0

    @class_rpc
    async def print_message(self, message: str) -> None:
        self.messages_count += 1
        print(f"Alice said: \"{message}\". Total: {self.messages_count} message(s).")


service = BobService("localhost", 5678)


async def main():
    await service.start()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
