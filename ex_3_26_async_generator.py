import asyncio
from aioredis import from_url


async def do_something_with(value):
    await asyncio.sleep(0)
    return int(value)


# Функция main() идентична версии в примере 3_25.
async def main():
    redis = from_url('redis://localhost')
    keys = ['Americas', 'Africa', 'Europe', 'Asia']

    # Ну, почти идентично: название изменено с camelCase на snake_case.
    async for value in one_at_a_time(redis, keys):
        await do_something_with(value)


# Наша функция теперь объявлена с помощью async def, что делает ее функцией сопрограммы,
# и поскольку эта функция также содержит ключевое слово yield, мы называем ее асинхронной
# генераторной функцией.
async def one_at_a_time(redis, keys):
    for k in keys:
        # Нам не нужно выполнять сложные действия, необходимые в предыдущем примере с self.ikeys:
        # здесь мы просто перебираем ключи напрямую и получаем значение...
        value = await redis.get(k)
        # ...а затем передаем его вызывающему коду, точно так же, как обычный генератор.
        yield value


if __name__ == '__main__':
    asyncio.run(main())
