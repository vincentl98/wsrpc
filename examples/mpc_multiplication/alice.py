import asyncio
import random
from asyncio import Future
from typing import Tuple

from examples.mpc_multiplication import stephanie, bob
from wsrpc import rpc, Service

service = Service("localhost", 6789)


@rpc(service)
async def set_daniel_shares(shares: Tuple[int, int, int]) -> None:
    print(f"Received shares from Daniel: {shares}")
    s_0.set_result(shares[0])
    t_0.set_result(shares[1])
    st_0.set_result(shares[2])


@rpc(service)
async def set_stephanie_share(share: int) -> None:
    b_0.set_result(share)


@rpc(service)
async def set_alpha_beta(values: Tuple[int, int]) -> None:
    alpha.set_result(values[0])
    beta.set_result(values[1])


async def main():
    a = 5
    r = random.randint(0, 100)
    a_0 = a - r
    a_1 = r

    await service.start()

    await stephanie.set_alice_share(a_1)

    alpha_0 = a_0 - await s_0
    beta_0 = await b_0 - await t_0

    print(f"a_0 = {a_0}, b_0 = {await b_0}")

    print(f"alpha_0 = {alpha_0}, beta_0 = {beta_0}")
    await stephanie.set_alpha_beta_shares((alpha_0, beta_0))

    z_0 = await alpha * await beta + await alpha * await t_0 + await beta * await s_0 + await st_0
    await bob.set_alice_value(z_0)


if __name__ == "__main__":
    b_0 = Future()
    s_0 = Future()
    t_0 = Future()
    st_0 = Future()
    alpha_1 = Future()
    beta_1 = Future()
    alpha = Future()
    beta = Future()

    asyncio.get_event_loop().run_until_complete(main())
