import inspect
from typing import Callable, Any, Union

from wsrpc.stateless_service import StatelessService

IS_REGISTERED = "_wsrpc_is_registered"


def rpc(fn_or_service: Union[Callable, StatelessService]) -> Callable:
    """ Mark a function as remotely callable.
    There are two different usages:
        - If used inside a `StateService`, use `@rpc` (returns a decorated function)
        - If used along with a regular `Service`, use `@rpc(service)` (returns a decorator)
    """

    if callable(fn_or_service):
        return _state_service_rpc(fn_or_service)  # returns a function
    else:
        assert isinstance(fn_or_service, StatelessService), f"Cannot decorate object `{fn_or_service}` because " \
                                                   f"it is not an instance or a subclass of `Service`."
        return _service_rpc(fn_or_service)  # returns a decorator


def _service_rpc(service: StatelessService) -> Callable[[Callable], Callable]:
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


def _state_service_rpc(fn: Callable) -> Callable:
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
