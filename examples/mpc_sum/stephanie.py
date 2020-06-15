import asyncio
from asyncio import Future
from typing import Optional

from wsrpc.decorators import rpc
from wsrpc.service import Service

service = Service("localhost", 6790)

if __name__ == "__main__":
    b = 200
    r: Optional[int] = None


@rpc(service)
async def set_r(new_r: int) -> None:
    global r
    r = new_r


@rpc(service)
async def encrypted_value() -> int:
    global r, b
    if r is None:
        raise Exception("Alice is not ready yet.")
    else:
        return b + r


async def main():
    await service.start()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())