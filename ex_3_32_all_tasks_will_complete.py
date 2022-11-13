import asyncio


async def f(delay):
    # Было бы ужасно, если бы кто-то передал нуль...
    await asyncio.sleep(1 / delay)
    return delay


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for i in range(10):
        loop.create_task(f(i))
    pending = asyncio.all_tasks(loop)
    group = asyncio.gather(*pending, return_exceptions=True)
    results = loop.run_until_complete(group)
    print(f'Results: {results}')
    loop.close()
    # Results: [5, 8, 6, 1, 2, ZeroDivisionError('division by zero'), 9, 7, 4, 3]
