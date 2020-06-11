import inspect
import pickle
from typing import Dict, Callable, Optional, Any

import websockets


class Service:

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._functions: Dict[str, Callable] = dict()
        self._server: Optional[websockets.WebSocketServer] = None

    async def _ws_handler(self, ws: websockets.WebSocketServerProtocol, path: str):
        async for message in ws:
            fn_name, args, kwargs = pickle.loads(message)

            assert fn_name in self._functions
            fn = self._functions[fn_name]

            if args is None:
                args = []

            if kwargs is None:
                kwargs = {}

            try:
                if inspect.iscoroutinefunction(fn):
                    value = await fn(*args, _rpc=False, **kwargs)
                else:
                    value = fn(*args, _rpc=False, **kwargs)
                ok = True
            except Exception as e:
                value = e
                ok = False

            await ws.send(pickle.dumps((ok, value)))

    async def start(self) -> None:
        assert self._server is None
        self._server = await websockets.serve(self._ws_handler, host=self._host,
                                              port=self._port)

    async def stop(self) -> None:
        assert self._server is not None
        self._server.stop()
        await self._server.wait_closed()
        self._server = None

    def register_rpc(self, fn: Callable, fn_name: Optional[str] = None) -> None:
        if fn_name is None:
            fn_name = fn.__name__
        assert fn_name not in self._functions.keys(), f"\"{fn_name}\" is already registered."
        self._functions[fn_name] = fn

    def _root_uri(self) -> str:
        return f"ws://{self._host}:{self._port}"

    def call_local_fn(self, fn_name: str, *args, **kwargs) -> Any:
        assert fn_name in self._functions

        return self._functions[fn_name](*args, **kwargs)

    async def call_remote_fn(self, fn_name: str, *args, **kwargs) -> Any:
        assert fn_name in self._functions

        async with websockets.connect(self._root_uri()) as ws:
            serialized_args = pickle.dumps((fn_name, args, kwargs))
            await ws.send(serialized_args)
            message = await ws.recv()
            ok, result = pickle.loads(message)

            if not ok:
                raise result
            else:
                return result
