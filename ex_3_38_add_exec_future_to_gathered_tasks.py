import time
import asyncio


# Эта служебная функция make_coro() просто ожидает завершения future - но, что важно, она
# продолжает ожидать future даже внутри обработчика исключений для CancelledError.
async def make_coro(future):
    try:
        return await future
    except asyncio.CancelledError:
        return await future


async def main():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking)
    # Мы берем объект future, возвращенный из вызова run_in_executor(), и передаем его в новую
    # служебную функцию make_coro(). Важным моментом здесь является то, что мы используем
    # create_task(), что означает, что эта задача появится в списке all_tasks() в рамках
    # обработки завершения работы asyncio.run() и получит отмену во время процесса
    # завершения работы.
    asyncio.create_task(make_coro(future))
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


def blocking():
    time.sleep(2.0)
    print(f'{time.ctime()} Hello from a thread!')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bye!')
