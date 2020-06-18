import inspect
from typing import Callable, Any

from wsrpc.service import Service

IS_REGISTERED = "_wsrpc_is_registered"


def rpc(service: Service):
    assert type(service) is Service, "Cannot use `rpc` decorator with objects with a type different of `Service`. " \
                                     "If you are using a `StateService`, use `class_rpc` instead."

    def decorator(fn: Callable):
        fn_name = fn.__name__

        if not inspect.iscoroutinefunction(fn):
            raise Exception(f"Function {fn_name} cannot be registered as a remote call function "
                            f"because it is not async.")

        async def decide_and_call(*args, _wsrpc_is_remote_call=True, **kwargs) -> Any:
            if not _wsrpc_is_remote_call:
                return await fn(*args, **kwargs)
            else:
                return await service.call_remote_fn(fn_name, *args, **kwargs)

        service.register_fn(decide_and_call, fn_name=fn_name)
        setattr(decide_and_call, IS_REGISTERED, True)
        return decide_and_call

    return decorator


def class_rpc(fn: Callable):
    fn_name = fn.__name__

    if not inspect.iscoroutinefunction(fn):
        raise Exception(f"Function {fn_name} cannot be registered as a remote call function "
                        f"because it is not async.")

    async def decide_and_call(self, *args, _wsrpc_is_remote_call=True, **kwargs) -> Any:

        if not _wsrpc_is_remote_call:
            return await fn(self, *args, **kwargs)
        else:
            return await self.call_remote_fn(fn_name, *args, **kwargs)

    setattr(decide_and_call, IS_REGISTERED, True)

    return decide_and_call
