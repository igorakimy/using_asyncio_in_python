import asyncio


async def f():
    try:
        while True:
            await asyncio.sleep(0)
    # Наша функция сопрограммы теперь обрабатывает исключение. Фактически, она обрабатывает
    # конкретный тип исключения - asyncio.CancelledError, используемый в библиотеке asyncio
    # для отмены задачи. Обратите внимание, что исключение вводится в сопрограмму извне;
    # т.е. с помощью цикла событий, который мы все еще имитируем с помощью команд send() и
    # throw() вручную. В реальном коде CancelledError вызывается внутри сопрограммы,
    # обернутой в задачу, когда задачи отменяются.
    except asyncio.CancelledError:
        # Простое сообщение о том, что задание было отменено. Обратите внимание, что
        # обрабатывая исключение, мы гарантируем, что оно больше не будет распространяться,
        # и наша сопрограмма вернется.
        print('I was cancelled!')
    else:
        return 123


if __name__ == '__main__':
    coro = f()

    coro.send(None)
    coro.send(None)
    # Здесь бросается исключение asyncio.CancelledError.
    coro.throw(asyncio.CancelledError)
    # Как и ожидалось, мы видим, что печатается наше сообщение об отмене.

    # I was cancelled!
    # Traceback (most recent call last):
    #   File "<stdin>", line 19, in <module>
    #     coro.throw(asyncio.CancelledError)

    # Наша сопрограмма завершается нормально. (Напомним, что исключение StopIteration -
    # это обычный способ выхода сопрограмм.)

    # StopIteration
