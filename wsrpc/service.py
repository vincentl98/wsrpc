import inspect
import pickle
from typing import Optional

import websockets

from wsrpc.service_api import ServiceApi


class InvalidArgumentsLengthError(Exception):
    pass


class InvalidFunctionError(Exception):
    pass


class Service:

    def __init__(self, service_api: ServiceApi) -> None:
        self._service_api = service_api
        self._server: Optional[websockets.WebSocketServer] = None

    async def ws_handler(self, ws: websockets.WebSocketServerProtocol, path: str):
        async for message in ws:
            fn_name, args = pickle.loads(message)

            if self._service_api.has_fn(fn_name):
                fn = self._service_api.ref(fn_name)

                if args is None:
                    args = []

                signature = inspect.signature(fn)

                if len(args) == len(signature.parameters):
                    try:
                        if inspect.iscoroutinefunction(fn):
                            value = await fn(*args)
                        else:
                            value = fn(*args)
                        ok = True
                    except Exception as e:
                        value = e
                        ok = False
                else:
                    value = InvalidArgumentsLengthError()
                    ok = False
            else:
                value = InvalidFunctionError()
                ok = False
            await ws.send(pickle.dumps((ok, value)))

    async def open(self) -> None:
        assert self._server is None
        self._server = await websockets.serve(self.ws_handler, host=self._service_api.host(),
                                              port=self._service_api.port())

    async def close(self) -> None:
        assert self._server is not None
        self._server.close()
        await self._server.wait_closed()
        self._server = None
