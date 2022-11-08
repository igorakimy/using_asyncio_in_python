import asyncio


async def coro():
    await asyncio.sleep(0)
    return 111


async def f():
    for _ in range(10):
        asyncio.create_task(coro())


if __name__ == '__main__':
    asyncio.run(f())
