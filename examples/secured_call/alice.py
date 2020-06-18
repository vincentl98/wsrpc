import asyncio
import tensorflow as tf
import bob
import exceptions


async def main():
    tensor = tf.constant([1], shape=(1,))
    try:
        await bob.print_message(tensor)  # Will throw an error, because we're not authenticated
    except exceptions.InvalidTokenError as e:
        print("Bob rejected our remote call.")

    try:
        await bob.print_message(tensor, token="alice_token_123")
        print("Bob accepted our remote call.")
    except exceptions.InvalidTokenError as e:
        print("Bob rejected our remote call.")  # Should not be printed


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
