import inspect
import dill
import ssl
from typing import Dict, Callable, Optional, Any

import websockets


class Service:
    """ A class wrapping a WebSocket server to be used for remote function call.
    Acts both as a client and a server. To register a function as remotely callable, use `rpc` decorator
    as follows: `@rpc(service)`.
    """

    def __init__(self, host: str, port: int, ssl_certificate_filename: Optional[str] = None) -> None:
        self._host = host
        self._port = port
        self._functions: Dict[str, Callable] = dict()
        self._server: Optional[websockets.WebSocketServer] = None
        self._ssl_certificate_path = ssl_certificate_filename

    async def _ws_handler(self, ws: websockets.WebSocketServerProtocol, path: str):

        async for message in ws:
            fn_name, args, kwargs = dill.loads(message)

            assert fn_name in self._functions, f"Function {fn_name} cannot be called because it is not registered. " \
                                               f"Try using `rpc` decorator."

            fn = self._functions[fn_name]

            if args is None:
                args = []

            if kwargs is None:
                kwargs = {}

            try:
                if inspect.iscoroutinefunction(fn):
                    value = await fn(*args, _wsrpc_is_remote_call=False, **kwargs)
                else:
                    value = fn(*args, _wsrpc_is_remote_call=False, **kwargs)
                ok = True
            except Exception as e:
                value = e
                ok = False

            await ws.send(dill.dumps((ok, value), byref=True))

    def is_started(self) -> bool:
        return self._server is not None

    async def start(self) -> None:
        assert not self.is_started()
        assert len(self._functions.keys()) > 0, "Cannot start service because no function has been registered."

        if self._ssl_certificate_path is not None:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(self._ssl_certificate_path)
        else:
            ssl_context = None
        self._server = await websockets.serve(self._ws_handler, host=self._host,
                                              port=self._port, ssl=ssl_context)

    async def stop(self) -> None:
        assert self.is_started()
        self._server.stop()
        await self._server.wait_closed()
        self._server = None

    def register_fn(self, fn: Callable, fn_name: Optional[str] = None) -> None:
        if fn_name is None:
            fn_name = fn.__name__
        assert fn_name not in self._functions.keys(), f"Cannot register function {fn_name} because another function" \
                                                      f"having the same name is already registered."
        self._functions[fn_name] = fn

    def _root_uri(self) -> str:
        if self._ssl_certificate_path is not None:
            return f"wss://{self._host}:{self._port}"
        else:
            return f"ws://{self._host}:{self._port}"

    def call_local_fn(self, fn_name: str, *args, **kwargs) -> Any:
        assert fn_name in self._functions

        return self._functions[fn_name](*args, **kwargs)

    async def call_remote_fn(self, fn_name: str, *args, **kwargs) -> Any:
        assert fn_name in self._functions, f"Function {fn_name} is not registered."

        if self._ssl_certificate_path is not None:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_verify_locations(self._ssl_certificate_path)
        else:
            ssl_context = None

        async with websockets.connect(self._root_uri(), ssl=ssl_context) as ws:
            serialized_args = dill.dumps((fn_name, args, kwargs), byref=True)
            await ws.send(serialized_args)
            message = await ws.recv()
            try:
                ok, result = dill.loads(message)
            except AttributeError as e:
                raise AttributeError("This error is likely due to different class names during "
                                     "serialization and deserialization of function remote call response. "
                                     "Check that the imports and names are identical in the function definition "
                                     "context and in the function call context. For more information, "
                                     "check Dill's documentation.") from e
            if not ok:
                raise result
            else:
                return result
