import asyncio
import examples.secured_call.bob as bob
import examples.secured_call.exceptions


async def get_and_send_message():
    message = input("Please type a message for Bob:")
    await bob.print_message(message)


async def main():
    message = "Hello from Alice!"
    try:
        await bob.print_message(message)  # Will throw an error, because we're not authenticated
    except examples.secured_call.exceptions.InvalidTokenError as e:
        print("Bob rejected our remote call.")

    try:
        await bob.print_message(message, token="alice_token_123")
        print("Bob accepted our remote call.")
    except examples.secured_call.exceptions.InvalidTokenError as e:
        print("Bob rejected our remote call.")  # Should not be printed


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
