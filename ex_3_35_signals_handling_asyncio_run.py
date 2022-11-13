import asyncio
from signal import SIGINT, SIGTERM


async def main():
    loop = asyncio.get_running_loop()
    for sig in (SIGINT, SIGTERM):
        # Поскольку asyncio.run() управляет запуском цикла событий, наша первая возможность
        # изменить поведение обработки сигналов будет в функции main().
        loop.add_signal_handler(sig, handler, sig)

    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        for i in range(3):
            print('<Your app is shutting down...>')
            await asyncio.sleep(1)


def handler(sig):
    loop = asyncio.get_running_loop()
    # Внутри обработчика сигналов мы не можем остановить цикл событий, как в предыдущих примерах,
    # потому что мы получим предупреждение о том, как цикл был остановлен до завершения задачи,
    # созданной для main(). Вместо этого мы можем инициировать отмену задачи здесь, что в конечном
    # итоге приведет к завершению задачи main(); когда это произойдет, процесс очистки внутри
    # asyncio.run() вступит в силу.
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()
    print(f'Got signal: {sig!s}, shutting down.')
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)


if __name__ == '__main__':
    asyncio.run(main())
