import asyncio
from asyncio import Future
from typing import Tuple
import numpy as np

from wsrpc import rpc, Service

import bob
import stephanie


class AliceService(Service):

    def __init__(self) -> None:
        super().__init__("localhost", 6789)

        self._matrix = None

        self.alpha = Future()
        self.beta = Future()
        self.daniel_shares = Future()
        self.stephanie_share = Future()

        self.is_finished = Future()
        self.is_finished.set_result(True)

    async def set_matrix(self, matrix: np.ndarray) -> None:
        await self.is_finished
        self.reset()
        self._matrix = matrix

    def reset(self) -> None:
        self.alpha = Future()
        self.beta = Future()
        self.daniel_shares = Future()
        self.stephanie_share = Future()

    @rpc
    async def matrix_shape(self) -> Tuple[int, int]:
        assert self._matrix is not None, "Cannot return matrix shape because it has not been set."
        return self._matrix.shape

    @rpc
    async def set_daniel_shares(self, shares: np.ndarray) -> None:
        self.daniel_shares.set_result(shares)

    @rpc
    async def set_alpha_beta(self, alpha: np.ndarray, beta: np.ndarray) -> None:
        self.alpha.set_result(alpha)
        self.beta.set_result(beta)

    @rpc
    async def set_stephanie_share(self, share: int) -> None:
        self.stephanie_share.set_result(share)  # a_1

    async def matrix_multiplication_share(self) -> np.ndarray:
        self.is_finished = Future()

        assert self._matrix is not None, "Cannot generate matrix multiplication share because no matrix was set."
        n, p_ = self._matrix.shape
        p, q = await stephanie.service.matrix_shape()
        assert p == p_
        print(f"n,p,q = {n},{p},{q}")

        r = np.random.randint(0, high=100)

        print(f"alice shares for stephanie = {r}")
        await stephanie.service.set_alice_share(r)

        s, t, st = await self.daniel_shares

        print(f"received s,t,st = {s},{t},{st}")

        alpha_shares = np.zeros((n, q, p))
        beta_shares = np.zeros((n, q, p))

        a_0 = np.zeros((n, q, p))
        for i in range(n):
            for j in range(q):
                for k in range(p):
                    a_0[i, j, k] = self._matrix[i, k] - r

        for i in range(n):
            for j in range(q):
                for k in range(p):
                    alpha_shares[i, j, k] = a_0[i, j, k] - s
                    beta_shares[i, j, k] = await self.stephanie_share - t

        await stephanie.service.set_alpha_beta_shares(alpha_shares, beta_shares)

        shares = await self.alpha * await self.beta + \
                 await self.alpha * t + \
                 await self.beta * s + st

        self.is_finished.set_result(True)

        return shares.sum(axis=2)


service = AliceService()


async def main():
    await service.start()
    await service.set_matrix(np.array([[1, 2],
                                       [3, 4]]))

    share = await service.matrix_multiplication_share()
    await bob.service.set_alice_value(share)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
