import asyncio
from asyncio import Future
from typing import Callable

from wsrpc import service_api
from wsrpc.service import Service


def hello() -> str:
    return "Hello World !"


def add(a: int, b: int) -> int:
    return a + b


def echo(message: str) -> str:
    return message


api = service_api.ServiceApi("localhost", 6789, {
    hello: Callable[[], str],
    add: Callable[[int, int], int],
    echo: Callable[[str], str]
})


async def main():
    await Service(api).open()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
