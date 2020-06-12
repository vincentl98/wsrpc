# wsrpc
A remote function call library designed for microservices.
Using Python, WebSocket and Pickle.

## Sample code

### User manager service `user_manager.py`
```python
from wsrpc.service import Service
from wsrpc.decorators import rpc

service = Service("localhost", 6789)

users: List[Tuple[str, str]] = []

@rpc(service)
async def add_user(user: (str, str)) -> None:
    users.append(user)

@rpc(service)
async def get_user(username: str) -> (str, str):
    for user in users:
        if user[0] == username:
            return user
    raise Exception("User not found")

async def main():
    await service.start()
    await Future() # never finishes

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
```

### Client

```python
import user_manager

username = input()

await user_manager.add((username, "password")) # remote call
user = await user_manager.get_user(username) # also remote call
```

## Tutorial
Let's say we want to have a user manager service, that
handles any change in the user database. For sake of simplicity,
users are 
stored as a list of tuples of string containing 
username and password. We can define the `users` list as follow:

```python
users: List[Tuple[str, str]] = []
```

Then, we can create the WebSocket server that
will handle incoming remote calls. It is wrapped under a `Service`
object that handles anything related to the function calls. We
must specify hostname and port:
```python
from wsrpc.service import Service

service = Service("localhost", 6789)
```

Before actually running it, we will need to define
and add the functions that will be remotely called.
Let's add one function to add a user, and one function 
to retrieve and existing user:

```python
from wsrpc.decorators import rpc

@rpc(service)
async def add_user(user: (str, str)) -> None:
    users.append(user)

@rpc(service)
async def get_user(username: str) -> (str, str):
    for user in users:
        if user[0] == username:
            return user
    raise Exception("User not found")
```

Remotely callable functions should be both `async`
and decorated with `@rpc(service)`. 


What it does under the hood is registering the 
function as a remote method inside the `service`
object, and then adding some additional code to
handle both local and remote calls. Because it 
cannot know beforehand if the function will be 
called from the service local machine or from a remote client one,
it is therefore mandatory to tag it as `async` 
even though it might not actually be `async` in case
of a local execution of a non-async function. 
Not tagging a function `async` will result in a parse-time
error.

A function not decorated with `@rpc` will be 
a regular function. It can be helpful when not 
wanting to make a function public, or if the method is 
static with regards to the service (in this case, the function
can be executed directly on the remote machine):

```python
def check_username_length(username: str) -> bool:
    return len(username) > 5
```

Finally, we can start the service:

```python
async def main():
    await service.start()
    await Future() # never finishes

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
```
From another machine, we can easily call the 
remote functions with no additional syntax:

```python
import user_manager

username = input()

if user_manager.check_username_length(username): # local call
    await user_manager.add((username, "password")) # remote call
    user = await user_manager.get_user(username) # also remote call
```

It is important to note that whether the call is remote or local 
only depends
 on the `@rpc` decorator. In some cases, we also want to call a 
decorated function locally (e.g. in the service internal code).
Service object provides such ability:

```python
user = await service.call_local_fn("get_user", "my_cool_username")
```

However it is not recommended since type hints are not available.

## Notes
- Does not support other language than Python