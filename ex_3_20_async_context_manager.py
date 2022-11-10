import asyncio


class Socket:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def close(self):
        print(f'Connection closed on {self.host}:{self.port}')
        return True


async def get_conn(host, port):
    return Socket(host, port)


class Connection:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    # Вместо специального метода __enter__() для синхронных контекстных менеджеров используется
    # новый специальный метод __aenter__(). Этот специальный метод должен начинаться с async def.
    async def __aenter__(self):
        self.conn = await get_conn(self.host, self.port)
        return self.conn

    # Аналогично вместо __exit__() используйте __aexit__(). Параметры идентичны параметрам __exit__()
    # и заполняются, если в теле контекстного менеджера было вызвано исключение.
    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


async def main():
    async with Connection('localhost', 9001) as conn:
        ...


if __name__ == '__main__':
    asyncio.run(main())
    # Connection closed on localhost:9001
