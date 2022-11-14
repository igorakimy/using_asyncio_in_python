import time
import asyncio


async def main():
    loop = asyncio.get_running_loop()
    # Идея направлена на исправление недостатка, заключающегося в том, что run_in_executor()
    # возвращает только экземпляр Future, а не задачу. Мы не можем зафиксировать задание в
    # all_tasks() (используется в asyncio.run()), но мы можем использовать await во future.
    # Первая часть плана состоит в том, чтобы создать будущее внутри функции main().
    future = loop.run_in_executor(None, blocking)
    try:
        print(f'{time.ctime()} Hello!')
        await asyncio.sleep(1.0)
        print(f'{time.ctime()} Goodbye!')
    finally:
        # Мы можем использовать структуру try/finally, чтобы гарантировать, что мы дождемся
        # завершения future до возврата функции main().
        await future


def blocking():
    time.sleep(2.0)
    print(f'{time.ctime()} Hello from a thread!')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bye!')
