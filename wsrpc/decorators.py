import inspect
from typing import Callable, Any

from wsrpc.service import Service


def rpc(service: Service):
    def decorator(fn: Callable):
        fn_name = fn.__name__

        if not inspect.iscoroutinefunction(fn):
            raise Exception(f"Function {fn_name} should be async to be used along with rpc decorator.")

        async def decide_and_call(*args, _wsrpc_is_remote_call=True, **kwargs) -> Any:
            if not _wsrpc_is_remote_call:
                return await fn(*args, **kwargs)
            else:
                return await service.call_remote_fn(fn_name, *args, **kwargs)

        service.register_rpc(decide_and_call, fn_name=fn_name)
        return decide_and_call

    return decorator
