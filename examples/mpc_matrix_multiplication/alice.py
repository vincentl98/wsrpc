import asyncio
from asyncio import Future
from typing import Tuple

import numpy as np

import examples.mpc_matrix_multiplication.bob as bob
import examples.mpc_matrix_multiplication.stephanie as stephanie
from wsrpc import rpc, Service


class AliceService(Service):

    def __init__(self):
        super().__init__("localhost", 6789)

        self.matrix = np.array([[1, 2]])

        self.alpha = Future()
        self.beta = Future()
        self.daniel_shares = Future()
        self.stephanie_shares = Future()

    @rpc
    async def matrix_shape(self) -> Tuple[int, int]:
        return self.matrix.shape

    @rpc
    async def set_daniel_shares(self, shares: np.ndarray) -> None:
        self.daniel_shares.set_result(shares)

    @rpc
    async def set_alpha_beta(self, alpha: np.ndarray, beta: np.ndarray) -> None:
        self.alpha.set_result(alpha)
        self.beta.set_result(beta)

    @rpc
    async def set_stephanie_shares(self, shares: np.ndarray) -> None:
        self.stephanie_shares.set_result(shares)  # a_1

    async def z_0(self):
        n, p_ = self.matrix.shape
        p, q = await stephanie.service.matrix_shape()
        assert p == p_
        print(f"n,p,q = {n},{p},{q}")

        r = np.random.randint(0, 100, n * q * p).reshape((n, q, p))

        print(f"alice shares for stephanie = {r}")
        await stephanie.service.set_alice_shares(r)

        s, t, st = await self.daniel_shares

        print(f"received s,t,st = {s},{t},{st}")

        alpha_shares = np.zeros((n, q, p))
        beta_shares = np.zeros((n, q, p))

        a_0 = np.zeros((n, q, p))
        for i in range(n):
            for j in range(q):
                for k in range(p):
                    a_0[i, j, k] = self.matrix[i, k] - r[i, j, k]

        for i in range(n):
            for j in range(q):
                for k in range(p):
                    alpha_shares[i, j, k] = a_0[i, j, k] - s
                    beta_shares[i, j, k] = (await self.stephanie_shares)[i, j, k] - t

        await stephanie.service.set_alpha_beta_shares(alpha_shares, beta_shares)

        shares = await self.alpha * await self.beta + \
                 await self.alpha * t + \
                 await self.beta * s + st
        return shares.sum(axis=2)


service = AliceService()


async def main():
    await service.start()
    await bob.service.set_alice_value(await service.z_0())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
