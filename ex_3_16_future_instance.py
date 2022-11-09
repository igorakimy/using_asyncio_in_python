import asyncio


# Создается простая функция main. Мы можем запустить ее, немного подождать, а затем
# установить результат для параметра f c типом Future.
async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    # Установить результат.
    f.set_result('I have finished.')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Вручную создается экземпляр Future. Обратите внимание, что этот экземпляр
    # (по умолчанию) привязан к нашему циклу, но он не привязан и не будет привязан
    # ни к одной сопрограмме (для этого предназначены экземпляры Task).
    fut = asyncio.Future()

    # Прежде чем что-либо делать, убедиться, что будущий объект еще не завершен.
    print(fut.done())
    # False

    # Запланировать сопрограмму main, передав ей объект Future. Помните, что все что делает
    # сопрограмма main() так это спит, а потом переключает экземпляр Future. (Обратите
    # внимание, что сопрограмма main() еще не начнет выполняться: сопрограммы выполняются
    # только когда цикл событий запущен).
    task = loop.create_task(main(fut))
    print(task)
    # <Task pending name='Task-1' coro=<main() running at <stdin>:4>>

    # Здесь мы используем run_until_complete() для экземпляра Future, а не для экземпляра Task.
    # Это отличается от того, что мы видели раньше. Теперь, когда цикл запущен, сопрограмма
    # main() начинает выполняться.
    result = loop.run_until_complete(fut)
    print(result)
    # I have finished.

    print(fut.done())
    # True

    # В конце концов, Future завершается, когда его результат установлен. После завершения можно
    # получить доступ к результату.
    print(fut.result())
    # I have finished.