import asyncio
from dataclasses import dataclass

import user_manager
from user import User


async def main():
    # await user_manager.add_user("vincent")
    vincent = await user_manager.get_user_by_username("vincent")
    print(vincent)
    # try:
    #     vincent = await user_manager.api.add_user("vincent")
    #
    #     print(vincent)
    # except NotFoundError as e:
    #     pass


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
