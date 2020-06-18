import asyncio

from examples.hello_world_class.bob import service as bob_service


async def main():
    await bob_service.print_message("First hello world!")
    await bob_service.print_message("Second hello world!")
    await bob_service.print_message("Third hello world!")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
