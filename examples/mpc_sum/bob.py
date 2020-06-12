import asyncio

import examples.mpc_sum.alice as alice
import examples.mpc_sum.stephanie as stephanie


async def main():
    alice_value = await alice.encrypted_value()
    stephanie_value = await stephanie.encrypted_value()
    print(f"Sum of Alice and Stephanie values: {alice_value + stephanie_value}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
