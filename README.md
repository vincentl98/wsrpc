# wsrpc
A **remote function call** library designed for ease of use.

*Warning*: this library is **highly experimental**.

Using **Python** (3.7+), **WebSocket** ([websockets](https://websockets.readthedocs.io/en/stable/) 8.1+) and **[dill](https://dill.readthedocs.io/en/latest/index.html)** 0.3.2+.
## Examples

See `examples` folder.

## Known limitations
- Only Python is supported
- As **dill** is being used for serialization, wsrpc has the same 
limitations concerning custom classes. See [dill documentation](https://dill.readthedocs.io/en/latest/index.html).
