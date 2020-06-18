import asyncio
import random
from asyncio import Future

from wsrpc import rpc, StatelessService

import stephanie

service = StatelessService("localhost", 6789)

if __name__ == "__main__":
    a = 100
    r = random.randint(0, 100)
    print(f"Random number r is set to {r}.")


@rpc(service)
async def encrypted_value() -> int:
    return a - r


async def main():
    await service.start()
    await stephanie.set_r(r)  # This is a remote call to stephanie's Service
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
