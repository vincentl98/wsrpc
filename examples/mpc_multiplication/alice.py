import asyncio
import random
from asyncio import Future
from typing import Tuple

from examples.mpc_multiplication import stephanie, bob
from wsrpc import rpc, Service


class AliceService(Service):

    def __init__(self):
        super().__init__("localhost", 6789)

        a = 5  # Secret number here

        self.alice_r = random.randint(0, 100)
        self.a_0 = a - self.alice_r
        self.a_1 = self.alice_r

        self.b_0 = Future()
        self.s_0 = Future()
        self.t_0 = Future()
        self.st_0 = Future()
        self.alpha = Future()
        self.beta = Future()

    @rpc
    async def set_daniel_shares(self, shares: Tuple[int, int, int]) -> None:
        self.s_0.set_result(shares[0])
        self.t_0.set_result(shares[1])
        self.st_0.set_result(shares[2])

    @rpc
    async def set_stephanie_share(self, share: int) -> None:
        self.b_0.set_result(share)

    @rpc
    async def set_alpha_beta(self, alpha_beta: Tuple[int, int]) -> None:
        self.alpha.set_result(alpha_beta[0])
        self.beta.set_result(alpha_beta[1])

    async def z_0(self) -> int:
        await stephanie.StephanieService().set_alice_share(self.a_1)

        alpha_0 = self.a_0 - await self.s_0
        beta_0 = await self.b_0 - await self.t_0

        await stephanie.StephanieService().set_alpha_beta_shares((alpha_0, beta_0))

        return await self.alpha * await self.beta + \
               await self.alpha * await self.t_0 + \
               await self.beta * await self.s_0 + await self.st_0


async def main():
    service = AliceService()
    await service.start()
    await bob.BobService().set_alice_value(await service.z_0())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
