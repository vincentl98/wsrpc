import asyncio
from asyncio import Future
from typing import Callable, Optional

from user import User
from wsrpc.service import Service, rpc

users = []

service = Service("localhost", 6789)


@rpc(service)
async def add_user(username: str, password: str = "abcd") -> None:
    if await has_user(username):
        raise Exception(f"User already exists: {username}")
    else:
        print(f"added user {username} {password}")
        users.append(User(username, password))


@rpc(service)
def get_user_by_username(username: str) -> User:
    for user in users:
        if user.username == username:
            return user
    raise Exception()


@rpc(service)
async def has_user(username: str) -> bool:
    for user in users:
        if user.username == username:
            return True
    return False


@rpc(service)
def remove_user(username: str) -> None:
    user = get_user_by_username(username)
    users.remove(user)


@rpc(service)
def update_username(old_username: str, new_username: str) -> None:
    user = get_user_by_username(old_username)
    user.username = new_username


async def main():
    await service.open()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
