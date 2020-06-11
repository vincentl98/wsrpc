import inspect
from typing import Callable, Any

from wsrpc.service import Service


def rpc(service_api: Service):
    def inner(fn: Callable):
        fn_name = fn.__name__

        if not inspect.iscoroutinefunction(fn):
            raise Exception(f"Function is not async: {fn_name}")

        async def decide_and_call(*args, _rpc=True, **kwargs) -> Any:

            if not _rpc:
                return await fn(*args, **kwargs)
            else:
                return await service_api.call_remote_fn(fn_name, *args, **kwargs)

        service_api.register_rpc(decide_and_call, fn_name=fn.__name__)
        return decide_and_call

    return inner
