import asyncio

import alice
import stephanie


async def main():
    alice_value = await alice.encrypted_value()  # This is a remote call

    ok = False
    stephanie_value = 0
    while ok is not True:
        try:
            stephanie_value = await stephanie.encrypted_value()  # This is a remote call
            ok = True
        except Exception as e:
            ok = False
            print("Stephanie is not ready yet.")
            await asyncio.sleep(1)

    print(f"Sum of Alice and Stephanie values: {alice_value + stephanie_value}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
