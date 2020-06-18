from __future__ import annotations

from typing import Optional
from wsrpc import StatelessService, decorators


class Service(StatelessService):
    """ A class wrapping a `Service` object having a state.

        Warning: this is HIGHLY EXPERIMENTAL.

        To register a function as remotely callable, use `rpc` decorator as follows: `@rpc`.
    """

    def __init__(self, host: str, port: int, ssl_certificate_filename: Optional[str] = None) -> None:
        super().__init__(host, port, ssl_certificate_filename=ssl_certificate_filename)
        self.update_registered_fns()

    def update_registered_fns(self):
        builtin_methods = [self.call_local_fn,
                           self.call_remote_fn,
                           self.is_started,
                           self.register_fn,
                           self.start,
                           self.stop,
                           self.update_registered_fns]

        registrable_methods = [method_name for method_name in dir(self)
                               if callable(getattr(self, method_name))
                               and not method_name.startswith("_")
                               and method_name not in map(lambda f: f.__name__, builtin_methods)]

        for method_name in registrable_methods:
            method = getattr(self, method_name)
            if getattr(method, decorators.IS_REGISTERED, False):
                self.register_fn(method, fn_name=method_name)
