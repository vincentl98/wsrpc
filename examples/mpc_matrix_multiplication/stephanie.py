import asyncio
from asyncio import Future
from typing import Tuple
import numpy as np
from wsrpc import rpc, Service

import alice
import bob


class StephanieService(Service):

    def __init__(self) -> None:
        super().__init__("localhost", 6790)

        self._matrix = None

        self.alice_shares = Future()
        self.alpha_0 = Future()
        self.beta_0 = Future()
        self.daniel_shares = Future()

        self.is_finished = Future()
        self.is_finished.set_result(True)

    async def set_matrix(self, matrix: np.ndarray) -> None:
        await self.is_finished
        self.reset()
        self._matrix = matrix

    def reset(self) -> None:
        self.alpha_0 = Future()
        self.beta_0 = Future()
        self.daniel_shares = Future()
        self.alice_shares = Future()

    @rpc
    async def matrix_shape(self) -> Tuple[int, int]:
        assert self._matrix is not None, "Cannot return matrix shape because it has not been set."
        return self._matrix.shape

    @rpc
    async def set_daniel_shares(self, shares: np.ndarray) -> None:
        self.daniel_shares.set_result(shares)

    @rpc
    async def set_alice_shares(self, shares: np.ndarray) -> None:
        self.alice_shares.set_result(shares)  # a_1

    @rpc
    async def set_alpha_beta_shares(self, alpha_shares: np.ndarray, beta_shares: np.ndarray) -> None:
        self.alpha_0.set_result(alpha_shares)
        self.beta_0.set_result(beta_shares)

    async def matrix_multiplication_share(self) -> int:
        self.is_finished = Future()

        assert self._matrix is not None, "Cannot generate matrix multiplication share because no matrix was set."
        n, p_ = await alice.service.matrix_shape()
        p, q = self._matrix.shape
        assert p == p_
        print(f"n,p,q = {n},{p},{q}")

        r = np.random.randint(0, 100, n * q * p).reshape((n, q, p))

        await alice.service.set_stephanie_shares(r)

        print(f"stephanie shares for alice : {r}")

        s, t, st = await self.daniel_shares

        print(f"received s,t,st = {s},{t},{st}")

        b_1 = np.zeros((n, q, p))
        for i in range(n):
            for j in range(q):
                for k in range(p):
                    b_1[i, j, k] = self._matrix[k, j] - r[i, j, k]

        alpha_1 = await self.alice_shares - s
        beta_1 = b_1 - t

        alpha = await self.alpha_0 + alpha_1
        beta = await self.beta_0 + beta_1

        await alice.service.set_alpha_beta(alpha, beta)

        shares = alpha * t + beta * s + st

        self.is_finished.set_result(True)

        return shares.sum(axis=2)


service = StephanieService()


async def main():
    await service.start()
    await service.set_matrix(np.array([[1, 2],
                                       [3, 4]]))
    share = await service.matrix_multiplication_share()
    await bob.service.set_stephanie_value(share)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
