import asyncio


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop2 = asyncio.get_event_loop()
    # Оба идентификатора, loop и loop2 ссылаются на один и тот же экземпляр.
    print(loop is loop2)
    # True
