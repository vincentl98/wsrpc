import asyncio

from examples import test_class


async def main():
    msg = await test_class.service.hello()
    print(msg)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
