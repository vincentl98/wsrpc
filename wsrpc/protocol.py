import asyncio
from typing import List, Iterable, Union, AsyncIterable, Any, Tuple

import websockets

Data = websockets.Data
Message = Union[Data, Iterable[Data], AsyncIterable[Data]]

CONNECTION_ERRORS = (OSError, ConnectionRefusedError, ConnectionAbortedError)


async def send_retry(uri: str, message: Message, retry_interval: float = 0.1, max_tries: int = 3) -> None:
    if max_tries == 0:
        raise ConnectionError()
    ok = await send(uri, message)
    if not ok:
        await asyncio.sleep(retry_interval)
        return await send_retry(uri, message, retry_interval=retry_interval, max_tries=max_tries - 1)


async def send(uri: str, message: Message) -> bool:
    try:
        async with websockets.connect(uri) as ws:
            await ws.send(message)
        return True
    except CONNECTION_ERRORS:
        return False
    except websockets.InvalidHandshake:
        try:
            await send_retry(uri, message)
            return True
        except ConnectionError:
            return False
