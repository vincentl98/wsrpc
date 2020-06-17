import asyncio
import random
from asyncio import Future
from typing import Tuple, Awaitable

from examples.mpc_multiplication import bob, alice
from wsrpc import rpc, Service

service = Service("localhost", 6790)


@rpc(service)
async def set_daniel_shares(shares: Tuple[int, int, int]) -> None:
    print(f"Received shares from Daniel: {shares}")
    s_1.set_result(shares[0])
    t_1.set_result(shares[1])
    st_1.set_result(shares[2])


@rpc(service)
async def set_alice_share(share: int) -> None:
    a_1.set_result(share)


@rpc(service)
async def set_alpha_beta_shares(shares: Tuple[int, int]) -> None:
    alpha_0.set_result(shares[0])
    beta_0.set_result(shares[1])


async def main():
    b = 12
    R = random.randint(0, 100)
    b_0 = R
    b_1 = b - R

    await service.start()

    await alice.set_stephanie_share(b_0)

    alpha_1 = await a_1 - await s_1
    beta_1 = b_1 - await t_1

    print(f"a_1 = {await a_1}, b_1 = {b_1}")

    print(f"alpha_1 = {alpha_1}, beta_1 = {beta_1}")

    alpha = await alpha_0 + alpha_1
    beta = await beta_0 + beta_1

    print(f"alpha = {alpha}, beta = {beta}")

    await alice.set_alpha_beta((alpha, beta))

    z_1 = alpha * await t_1 + beta * await s_1 + await st_1
    await bob.set_stephanie_value(z_1)


if __name__ == "__main__":
    a_1 = Future()
    s_1 = Future()
    t_1 = Future()
    st_1 = Future()
    alpha_0 = Future()
    beta_0 = Future()

    asyncio.get_event_loop().run_until_complete(main())
