import inspect
import pickle
import websockets
from typing import Dict, Type, Callable, Optional, Sequence, Any, Union


class ServiceApi:

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._functions: Dict[str, Callable] = dict()

    def register(self, fn: Callable) -> None:
        assert fn.__name__ not in self._functions.keys(), f"\"{fn.__name__}\" is already registered."
        self._functions[fn.__name__] = fn

    def ref(self, fn_name: str) -> Callable:
        assert self.has_fn(fn_name)
        return self._functions[fn_name]

    def root_uri(self) -> str:
        return f"ws://{self._host}:{self._port}"

    def host(self) -> str:
        return self._host

    def port(self) -> int:
        return self._port

    def has_fn(self, fn_name: str) -> bool:
        return fn_name in self._functions

    async def _call_remote_fn(self, fn: Union[Callable, str], args: Optional[Sequence[Any]] = None) -> Any:
        if type(fn) is not str:
            fn_name = fn.__name__
        else:
            fn_name = fn
        assert self.has_fn(fn_name)

        async with websockets.connect(self.root_uri()) as ws:
            serialized_args = pickle.dumps((fn_name, args))
            await ws.send(serialized_args)
            message = await ws.recv()
            ok, result = pickle.loads(message)

            if not ok:
                raise result
            else:
                return result

    def __getattr__(self, item: str) -> Callable[[Optional[Sequence[Any]]], Any]:
        assert item in self._functions.keys(), "Tried to call an nonexistent RPC: \"{item}\""
        return lambda *args: self._call_remote_fn(item, args)


def rpc(service_api: ServiceApi):
    def inner(fn: Callable):
        service_api.register(fn)
        return fn

    return inner
