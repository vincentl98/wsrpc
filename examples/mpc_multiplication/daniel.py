import asyncio
import random

import alice
import stephanie


async def main():
    s, t, u, v, w = [random.randint(0, 100) for _ in range(5)]

    s_shares = (s - u, u)
    t_shares = (t - v, v)
    st_shares = (s * t - w, w)

    alice_shares = (s_shares[0], t_shares[0], st_shares[0])
    stephanie_shares = (s_shares[1], t_shares[1], st_shares[1])

    await alice.AliceService().set_daniel_shares(alice_shares)
    await stephanie.StephanieService().set_daniel_shares(stephanie_shares)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
