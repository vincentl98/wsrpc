import asyncio
import random
from asyncio import Future

from wsrpc import rpc, Service

import examples.mpc_sum.stephanie as stephanie

service = Service("localhost", 6789)

if __name__ == "__main__":
    a = 100
    r = random.randint(0, 100)
    print(f"Random number r is set to {r}.")


@rpc(service)
async def encrypted_value() -> int:
    global a, r
    return a - r


async def main():
    global r
    await service.start()
    await stephanie.set_r(r)
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
