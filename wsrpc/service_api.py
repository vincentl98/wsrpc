import pickle
import websockets
from typing import Dict, Type, Callable, Optional, Iterable, Any


class ServiceApi:
    def __init__(self, host: str, port: int, functions: Dict[Callable, Type]) -> None:
        self._host = host
        self._port = port
        self._functions: Dict[str, (Callable, Type)] = dict()

        for fn, fn_type in functions.items():
            self._functions[fn.__name__] = (fn, fn_type)

    def host(self) -> str:
        return self._host

    def port(self) -> int:
        return self._port

    def type(self, fn_name: str) -> Type:
        assert self._has_fn(fn_name)
        return self._functions[fn_name][1]

    def ref(self, fn_name: str) -> Callable:
        assert self._has_fn(fn_name)
        return self._functions[fn_name][0]

    def _has_fn(self, fn_name: str) -> bool:
        return fn_name in self._functions

    def root_uri(self) -> (str, int):
        return f"ws://{self.host()}:{self.port()}"

    async def run(self, fn: Callable, args: Optional[Iterable[Any]] = None) -> Any:
        fn_name = fn.__name__
        assert self._has_fn(fn_name)

        async with websockets.connect(self.root_uri()) as ws:
            serialized_args = pickle.dumps((fn_name, args))
            await ws.send(serialized_args)
            message = await ws.recv()
            ok, result = pickle.loads(message)

            if not ok:
                raise result
            else:
                return result
