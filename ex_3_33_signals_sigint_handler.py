import asyncio


# Это основная часть нашего приложения. Чтобы все было проще, мы просто будем
# спать в бесконечном цикле.
async def main():
    while True:
        print('<Your app is running>')
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Мы планируем main(), вызываем run_forever() и ждем, пока что-нибудь
    # остановит цикл.
    task = loop.create_task(main())
    try:
        loop.run_until_complete(task)
    # В этом случает, только Ctrl-C остановит цикл. Затем мы обрабатываем
    # KeyboardInterrupt и выполняем битовые очистки.
    except KeyboardInterrupt:
        print('Got signal: SIGINT, shutting down.')
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
