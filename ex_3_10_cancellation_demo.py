import asyncio


async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        print('Nope!')
        # Вместо того чтобы печатать сообщение, что произойдет, если после отмены мы просто
        # вернемся к ожиданию другого ожидаемого?
        while True:
            await asyncio.sleep(0)
    else:
        return 123


if __name__ == '__main__':
    coro = f()

    coro.send(None)
    # Неудивительно, что наша внешняя сопрограмма продолжает жить и она немедленно снова
    # поддерживается внутри новой сопрограммы.
    coro.throw(asyncio.CancelledError)
    # Nope!

    # Все идет нормально, и наша сопрограмма продолжает приостанавливаться и возобновляться,
    # как и ожидалось.
    coro.send(None)
