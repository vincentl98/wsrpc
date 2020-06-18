import asyncio

import bob


async def main():
    await bob.service.print_message("First hello world!")
    await bob.service.print_message("Second hello world!")
    await bob.service.print_message("Third hello world!")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
