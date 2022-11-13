import asyncio
from asyncio import StreamReader, StreamWriter


# Эта функция сопрограммы echo() будет использоваться (сервером) для создания сопрограммы для
# каждого выполненного соединения. Функция использует стриминговое API для взаимодействия с asyncio.
async def echo(reader: StreamReader, writer: StreamWriter):
    print('New connection.')
    try:
        # Чтобы поддерживать соединение в рабочем состоянии, у нас будет бесконечный цикл
        # ожидания сообщений.
        while data := await reader.readline():
            # Вернуть данные обратно отправителю, но заглавными буквами.
            writer.write(data.upper())
            await writer.drain()
        print('Leaving connection.')
    # Если эта задача будет отменена, мы напечатаем сообщение.
    except asyncio.CancelledError:
        print('Connection dropped!')


# Этот код для запуска TCP-сервера взят непосредственно из документации Python 3.8.
async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bye!')
