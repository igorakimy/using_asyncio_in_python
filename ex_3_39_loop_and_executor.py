import time
import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor


async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')
    loop.stop()


def blocking():
    time.sleep(2.0)
    print(f'{time.ctime()} Hello from a thread!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # На этот раз мы создаем наш собственный экземпляр executor.
    executor = Executor()
    # Мы должны установить наш пользовательский исполнитель в качестве исполнителя по умолчанию
    # для цикла событий. Это означает, что везде, где код вызывает run_in_executor(), он будет
    # использовать наш пользовательский экземпляр.
    loop.set_default_executor(executor)
    loop.create_task(main())
    # Как и прежде, мы запускаем нашу блокирующую функцию.
    future = loop.run_in_executor(None, blocking)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Cancelled')
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    # Наконец, мы можем явно дождаться завершения всех заданий исполнителя, прежде чем закрывать
    # цикл. Это позволит избежать сообщений "Event loop is closed", которые мы видели раннее. Мы
    # можем сделать это, потому что у нас есть доступ к объекту executor; исполнитель по умолчанию
    # - не доступен в asyncio API, поэтому мы не можем вызывать shutdown() для него и были
    # вынуждены создать наш собственный экземпляр executor.
    executor.shutdown(wait=True)
    loop.close()
