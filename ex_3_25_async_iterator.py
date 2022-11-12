import asyncio
from aioredis import from_url


class OneAtATime:
    # Инициализатор этого класса довольно обычный: мы храним экземпляр подключения Redis
    # и список ключей для перебора.
    def __init__(self, redis, keys):
        self.redis = redis
        self.keys = keys

    # Используется __aiter__() для итерации.  Мы создаем обычный итератор по ключам self.ikeys
    # и возвращаем self, потому что OneAtATime также реализует метод сопрограммы __anext__().
    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self

    # Обратите внимание, что метод __anext__() объявляется с помощью async def, в то время как
    # метод __aiter__() объявляется только с помощью def.
    async def __anext__(self):
        try:
            # Для каждого ключа мы извлекаем значение из Redis: self.ikeys - это обычный итератор
            # по ключам, поэтому мы используем next() для перемещения по ним.
            k = next(self.ikeys)
        # Когда self.ikeys исчерпан, мы обрабатываем StopIteration и просто превращаем его в
        # StopAsyncIteration! Вот как вы сигнализируете об остановке внутри асинхронного итератора.
        except StopIteration:
            raise StopAsyncIteration

        # Наконец - весь смысл этого примера - мы можем получить данные из Redis, связанные с этим
        # ключом. Мы можем ожидать (await) данные, что означает, что другой код может выполняться
        # в цикле событий, пока мы ожидаем сетевой ввод-вывод.
        value = await self.redis.get(k)
        return value


async def do_something_with(value):
    await asyncio.sleep(0)
    return int(value)


# Функция main() запускается с помощью asyncio.run()
async def main():
    # Используется высокоуровневый интерфейс в aioredis для получения соединения.
    redis = await from_url('redis://localhost')
    # Представьте, что каждое из значений, связанных с этими ключами, довольно велико
    # и хранится в экземпляре Redis.
    keys = ['Americas', 'Africa', 'Europe', 'Asia']

    # Мы используем async for: дело в том, что итерация может приостанавливать саму себя
    # в ожидании поступления следующих данных.
    async for value in OneAtATime(redis, keys):
        # Для полноты картины представьте, что мы также выполняем некоторое действие, связанное
        # с вводом-выводом с извлеченным значением - возможно простое преобразование данных - и
        # затем оно отправляется к другому пункту назначения.
        await do_something_with(value)


if __name__ == '__main__':
    asyncio.run(main())
