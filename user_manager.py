import asyncio
from asyncio import Future
from typing import Callable, Optional

from user import User
from wsrpc import service_api
from wsrpc.service import Service
from wsrpc.service_api import ServiceApi, rpc

users = []

api = service_api.ServiceApi("localhost", 6789)


@rpc(api)
def add_user(username: str, password: str) -> None:
    print(f"added user {username} {password}")
    users.append(User(username, password))


@rpc(api)
def get_user_by_username(username: str) -> User:
    for user in users:
        if user.username == username:
            return user
    raise Exception()


@rpc(api)
def remove_user(username: str) -> None:
    user = get_user_by_username(username)
    users.remove(user)


@rpc(api)
def update_username(old_username: str, new_username: str) -> None:
    user = get_user_by_username(old_username)
    user.username = new_username


async def main():
    await Service(api).open()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
