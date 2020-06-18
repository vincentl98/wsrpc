import asyncio
import random
from asyncio import Future
from typing import Tuple
from wsrpc import rpc, Service

import alice
import bob


class StephanieService(Service):

    def __init__(self):
        super().__init__("localhost", 6790)

        b = 12  # Secret number here

        self.stephanie_r = random.randint(0, 100)
        self.b_0 = self.stephanie_r
        self.b_1 = b - self.stephanie_r

        self.a_1 = Future()
        self.s_1 = Future()
        self.t_1 = Future()
        self.st_1 = Future()
        self.alpha_0 = Future()
        self.beta_0 = Future()

    @rpc
    async def set_daniel_shares(self, shares: Tuple[int, int, int]) -> None:
        self.s_1.set_result(shares[0])
        self.t_1.set_result(shares[1])
        self.st_1.set_result(shares[2])

    @rpc
    async def set_alice_share(self, share: int) -> None:
        self.a_1.set_result(share)

    @rpc
    async def set_alpha_beta_shares(self, shares: Tuple[int, int]) -> None:
        self.alpha_0.set_result(shares[0])
        self.beta_0.set_result(shares[1])

    async def z_1(self) -> int:
        await alice.AliceService().set_stephanie_share(self.b_0)

        alpha_1 = await self.a_1 - await self.s_1
        beta_1 = self.b_1 - await self.t_1

        alpha = await self.alpha_0 + alpha_1
        beta = await self.beta_0 + beta_1

        await alice.AliceService().set_alpha_beta((alpha, beta))

        return alpha * await self.t_1 + beta * await self.s_1 + await self.st_1


async def main():
    service = StephanieService()
    await service.start()  # Starting the RPC server
    await bob.BobService().set_stephanie_value(await service.z_1())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
