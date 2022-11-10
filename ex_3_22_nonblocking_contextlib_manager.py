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


def process(data):
    print(data[:6])


# Новый декоратор @asynccontextmanager используется точно таким же образом.
@asynccontextmanager
# Однако для этого требуется, чтобы декорируемая генераторная функция была объявлена через async def.
async def web_url(url):
    # Как и прежде, мы извлекаем данные из URL-адреса, прежде чем сделать их доступными для тела
    # контекстного менеджера. Было добавлено ключевое слово await, которое сообщает нам, что эта
    # сопрограмма позволит циклу событий выполнять другие задачи, пока мы ждем пока завершится
    # сетевой вызов. Обратите внимание, что мы не можем просто привязать ключевое слово await к
    # чему-либо. Это изменение предполагает, что мы также смогли изменить саму функцию download_webpage()
    # и преобразовать ее в сопрограмму, совместимую с ключевым словом await. В тех случаях, когда
    # изменить функцию невозможно, необходим другой подход.
    data = await download_webpage(url)
    # Как и прежде, данные становятся доступными для тела контекстного менеджера. Я стараюсь, чтобы
    # код был простым, поэтому я опустил обычный обработчик try/finally, который обычно следует
    # писать для обработки исключений, возникающих в теле вызывающего объекта. Обратите внимание,
    # что наличие yield - это то, что превращает функцию в генераторную функцию; дополнительное
    # присутствие ключевых слов async def при объявлении делают эту функцию асинхронной генераторной
    # функцией. При вызове она вернет асинхронный генератор. Модуль inspect имеет две функции, которые
    # могут проверять их: isasyncgenfunction() и isasyncgen() соответственно.
    yield data
    # Здесь предположим, что мы также преобразовали код внутри функции update_stats(), чтобы
    # позволить ей создавать сопрограммы. Затем мы можем использовать ключевое слово await, которое
    # позволяет переключать контекст на цикл событий, пока мы ждем завершения работы, связанной
    # с вводом-выводом.
    await update_stats(url)


async def main():
    # Потребовалось еще одно изменение в использовании самого контекстного менеджера: нам нужно было
    # использовать async with вместо простого with.
    async with web_url('https://yandex.ru') as data:
        process(data)


if __name__ == '__main__':
    asyncio.run(main())