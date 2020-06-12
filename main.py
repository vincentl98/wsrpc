import asyncio
import user_manager


async def main():
    if not await user_manager.has()
    # await user_manager.add_user("vincent")
    vincent = await user_manager.get("vincent")
    print(vincent)
    # try:
    #     vincent = await user_manager.api.add_user("vincent")
    #
    #     print(vincent)
    # except NotFoundError as e:
    #     pass


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
