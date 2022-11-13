import asyncio
from asyncio import StreamReader, StreamWriter


# Представьте, что эта сопрограмма действительно связывается с внешним сервером
# для отправки уведомлений о событиях.
async def send_event(msg: str):
    await asyncio.sleep(1)
    return msg


async def echo(reader: StreamReader, writer: StreamWriter):
    print('New connection.')
    try:
        while data := await reader.readline():
            writer.write(data.upper())
            await writer.drain()
        print('Leaving connection.')
    except asyncio.CancelledError:
        msg = 'Connection dropped!'
        print(msg)
        # Поскольку средство уведомления о событиях включает доступ к сети, обычно
        # такие вызовы выполняются в отдельной асинхронной задаче; вот почему мы
        # используем здесь функцию create_task().
        asyncio.create_task(send_event(msg))


async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bye!')

    # Connection dropped!
    # Bye!
    # Task was destroyed but it is pending!
    # task: <Task pending name='Task-6' coro=<send_event() done,
    #   defined at <stdin>:5> wait_for=<Future pending cb=[Task.task_wakeup()]>>
