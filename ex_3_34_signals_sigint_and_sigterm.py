import asyncio
# Импорт значения сигнала из модуля signal стандартной библиотеки.
from signal import SIGINT, SIGTERM


async def main():
    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    # На этот раз наша сопрограмма main() собирается выполнить некоторую внутреннюю очистку.
    # Когда будет получен сигнал отмены (инициированный отменой каждой из задач), будет период
    # в 3 секунды, в течение которого main() будет продолжать выполняться во время фазы
    # run_until_complete() процесса завершения работы. Он будет печатать
    # <Your app is shutting down...>.
    except asyncio.CancelledError:
        for _ in range(3):
            print('<Your app is shutting down...>')
            await asyncio.sleep(1)


# Это обработчик обратного вызова, когда мы получаем сигнал. Он настраивается в цикле с
# помощью вызова add_signal_handler() немного ниже.
def handler(sig):
    # Основная цель обработчика - остановить цикл событий: это разблокирует вызов
    # loop.run_forever() и разрешит сбор и отмену ожидающих задач, а run_complete()
    # - для завершения работы.
    loop.stop()
    print(f'Got signal: {sig!s}, shutting down.')
    # Поскольку мы сейчас находимся в режиме завершения работы, мы не хотим, чтобы другой
    # SIGINT или SIGTERM снова запускал этот обработчик: это вызвало бы loop.stop() во время
    # фазы run_until_complete(), что помешало бы нашему процессу завершения. Поэтому мы
    # удаляем обработчик сигнала для SIGTERM из цикла событий.
    loop.remove_signal_handler(SIGTERM)
    # Это некая "уловка": мы не можем просто удалить обработчик для SIGINT, потому что, если
    # бы мы это сделали, KeyboardInterrupt снова стал бы обработчиком для SIGINT, таким же,
    # как это было до того, как мы добавили наши собственные обработчики. Вместо этого мы
    # устанавливаем пустую лямбда-функцию в качестве обработчика. Это означает, что
    # KeyboardInterrupt остается в стороне, а SIGINT (и Ctrl-C) не имеют никакого эффекта.
    loop.add_signal_handler(SIGINT, lambda: None)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Здесь обработчики сигналов были подключены к циклу событий. Обратите внимание, что,
    # как обсуждалось ранее, установка обработчика в SIGINT означает, что KeyboardInterrupt
    # больше не будет вызваться в SIGINT. Вызов KeyboardInterrupt является обработчиком
    # "по умолчанию" для SIGINT и предварительно настраивается в Python до тех пор, пока
    # вы не сделаете что-то, чтобы изменить обработчик.
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)
    loop.create_task(main())
    # Как обычно, выполнение блокируется на run_forever() до тех пор, пока что-то не
    # остановит цикл событий. В этом случае цикл будет остановлен внутри handler(), если
    # нашему процессу будет отправлен либо SIGINT, либо SIGTERM.
    loop.run_forever()
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
    # <Your app is running>
    # <Your app is running>
    # <Your app is running>
    # <Your app is running>
    # <Your app is running>
    # ^CGot signal: Signals.SIGINT, shutting down.
    # <Your app is shutting down...>
    # ^C<Your app is shutting down...>
    # ^C<Your app is shutting down...>
