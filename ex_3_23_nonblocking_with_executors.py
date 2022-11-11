from contextlib import asynccontextmanager
from httpx import AsyncClient
import asyncio


url_stat = {
    'https://yandex.ru': 0
}


async def download_webpage(url):
    async with AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
    return resp.text


async def update_stats(url):
    url_stat[url] = url_stat.get(url) + 1
    return 1


def process(data):
    print(data[:6])


@asynccontextmanager
# Для этого примера предположим, что мы не можем изменить код для наших двух блокирующих вызовов,
# download_webpage() и update_stats(); т.е. мы не можем изменить их, чтобы они были функциями
# сопрограммы. Это плохо, потому что самый тяжкий грех программирования на основе событий - это
# нарушение правила, согласно которому вы никогда, ни при каких обстоятельствах не должны
# препятствовать обработке событий циклом событий. Чтобы обойти проблему, мы будем использовать
# исполнителя для запуска блокирующих вызовов в отдельном потоке. Исполнитель становится
# доступным для нас как атрибут самого цикла событий.
async def web_url(url):
    loop = asyncio.get_event_loop()
    # Мы вызываем исполнителя. Сигнатура которого следующая: AbstractEventLoop.run_in_executor(
    # executor, func, *args). Если вы хотите использовать исполнителя по умолчанию (который
    # является ThreadPoolExecutor), вы должны передать None в качестве значения для аргумента
    # executor.
    data = await loop.run_in_executor(None, download_webpage, url)
    yield data
    # Как и в случае с вызовом download_webpage(), мы также запускаем другой блокирующий вызов
    # update_stats() в исполнителе. Обратите внимание, что вы должны использовать ключевое
    # слово await впереди. Если вы забыли, выполнение асинхронного генератора (т.е. вашего
    # асинхронного контекстного менеджера) не будет ждать завершения вызова, прежде чем
    # продолжить.
    await loop.run_in_executor(None, update_stats, url)


async def main():
    async with web_url('https://yandex.ru') as data:
        process(data)


if __name__ == '__main__':
    asyncio.run(main())
