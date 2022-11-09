import asyncio
from contextlib import suppress


async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    try:
        # f - переданный экземпляр Task. Он удовлетворяет сигнатуре типа функции (поскольку
        # Task является подклассом Future), но начиная с Python 3.8, нам больше не разрешатся
        # вызывать set_result() для задачи: попытка вызовет исключение RuntimeError. Идея
        # заключается в том, что объект класса Task представляет собой запущенную сопрограмму,
        # поэтому результат всегда должен исходить только из этого.
        f.set_result('I have finished.')
    except RuntimeError as e:
        print(f'No longer allowed: {e}')
        # Однако мы все равно можем вызвать метод cancel() у задачи, который вызовет исключение
        # CancelledError внутри базовой сопрограммы.
        f.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Единственное отличие заключается в том, что мы создаем экземпляр Task вместо Future.
    # Конечно, API Task требует от нас представления сопрограммы; мы просто используем
    # sleep(), потому что это удобно.
    fut = asyncio.Task(asyncio.sleep(1_000_000))
    print(fut.done())
    # False

    print(loop.create_task(main(fut)))
    # <Task pending name='Task-2' coro=<main() running at <stdin>:5>>

    with suppress(asyncio.CancelledError):
        loop.run_until_complete(fut)
    # No longer allowed: Task does not support set_result operation

    print(fut.done())
    # True

    print(fut.cancelled())
    # True
