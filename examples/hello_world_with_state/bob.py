import asyncio

from wsrpc import rpc, Service


class BobService(Service):

    def init_state(self) -> None:
        self.messages_count = 0

    @rpc
    async def print_message(self, message: str) -> None:
        self.messages_count += 1
        print(f"Alice said: \"{message}\". Total: {self.messages_count} message(s).")


service = BobService("localhost", 5678)


async def main():
    await service.start()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
