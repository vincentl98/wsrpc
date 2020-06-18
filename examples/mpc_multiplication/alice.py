import asyncio
import random
from asyncio import Future
from typing import Tuple

from examples.mpc_multiplication import stephanie, bob
from wsrpc import rpc, Service

service = Service("localhost", 6789)


@rpc(service)
async def set_daniel_shares(shares: Tuple[int, int, int]) -> None:
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
    a = 5  # Secret number here
    alice_r = random.randint(0, 100)
    a_0 = a - alice_r
    a_1 = alice_r

    # Setting up global variables that will be set during RPC calls to this machine
    global b_0, s_0, t_0, st_0, alpha, beta

    b_0 = Future()
    s_0 = Future()
    t_0 = Future()
    st_0 = Future()
    alpha = Future()
    beta = Future()

    await service.start()  # Starting the RPC server

    # Actual algorithm:
    await stephanie.set_alice_share(a_1)

    alpha_0 = a_0 - await s_0
    beta_0 = await b_0 - await t_0

    await stephanie.set_alpha_beta_shares((alpha_0, beta_0))

    z_0 = await alpha * await beta + await alpha * await t_0 + await beta * await s_0 + await st_0
    await bob.set_alice_value(z_0)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
