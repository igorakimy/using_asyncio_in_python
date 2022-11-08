import asyncio


async def f():
    await asyncio.sleep(0)
    return 111


if __name__ == '__main__':
    # Получаем цикл событий.
    loop = asyncio.get_event_loop()
    coro = f()
    # Запускаем сопрограмму до ее завершения. Внутренне это делает все тот же метод send(),
    # обнаруживая завершение нашей сопрограммы с помощью исключения StopIteration, которое
    # также содержит наше возвращаемое значение.
    print(loop.run_until_complete(coro))
    # 111
