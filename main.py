import asyncio

import calculation


async def main():
    hello_world = await calculation.api.run(calculation.hello)
    print(f"{hello_world}")
    result = await calculation.api.run(calculation.add, (2, 3))
    print(f"2 + 3 = {result} ")
    echo = await calculation.api.run(calculation.echo, ("Echo !",))
    print(f"{echo}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
