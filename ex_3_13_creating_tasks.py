import asyncio


async def coro1():
    await asyncio.sleep(1)
    return 111


async def f():
    loop = asyncio.get_event_loop()
    for _ in range(10):
        loop.create_task(coro1())


if __name__ == '__name__':
    asyncio.run(f())
