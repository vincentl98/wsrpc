import asyncio

import examples.hello_world.bob as bob


async def main():
    await bob.print_message("Hello world!")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
