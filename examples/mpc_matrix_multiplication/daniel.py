import asyncio
import numpy as np

import examples.mpc_matrix_multiplication.alice as alice
import examples.mpc_matrix_multiplication.stephanie as stephanie


async def main():
    s, t, u, v, w = np.random.randint(0, 100, 5)

    shares = np.array([[s - u, u],
                       [t - v, v],
                       [s * t - w, w]])

    alice_shares = shares[:, 0]
    stephanie_shares = shares[:, 1]
    print(f"alice_shares = {alice_shares}")
    print(f"stephanie_shares = {stephanie_shares}")
    await alice.service.set_daniel_shares(alice_shares)
    await stephanie.service.set_daniel_shares(stephanie_shares)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
