import asyncio
from asyncio import Future

from user import User
from wsrpc.decorators import rpc
from wsrpc.service import Service

users = []

service = Service("localhost", 6789)


@rpc(service)
async def add(username: str, password: str = "abcd") -> None:
    if contains(username):
        raise Exception(f"User already exists: {username}")
    else:
        print(f"added user {username} {password}")
        users.append(User(username, password))


@rpc(service)
async def get(username: str) -> User:
    for user in users:
        if user.username == username:
            return user
    raise Exception()


def contains(username: str) -> bool:
    for user in users:
        if user.username == username:
            return True
    return False


@rpc(service)
async def remove(username: str) -> None:
    user = get(username)
    users.remove(user)


@rpc(service)
async def update_username(old_username: str, new_username: str) -> None:
    user = get(old_username)
    user.username = new_username


async def main():
    await service.start()
    await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
