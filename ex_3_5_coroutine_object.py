import inspect


async def f():
    return 123


if __name__ == '__main__':
    coro = f()
    print(type(coro))
    # <class 'coroutine'>

    print(inspect.iscoroutine(coro))
    # True
