import asyncio


# Простая функция сопрограммы: ненадолго засыпает; затем возвращает значение параметра плюс 100.
async def f(x):
    await asyncio.sleep(.1)
    return x + 100


# Это асинхронный генератор, который мы вызываем внутри асинхронного спискового включения ниже,
# используя async for для управления итерацией.
async def factory(n):
    for x in range(n):
        await asyncio.sleep(.1)
        # Асинхронный генератор выдаст кортеж из f и переменной итерации x. Возвращаемое значение
        # f - это функция сопрограммы, но еще не сопрограмма.
        yield f, x


async def main():
    # Наконец, асинхронное списковое включение. Вызов factory(3) возвращает асинхронный генератор,
    # который должен управляться итерацией. Поскольку это асинхронный генератор, вы не можете
    # просто использовать for; вы должны использовать async for.
    # Значение, генерируемые асинхронным генератором, представляют собой кортеж сопрограммной
    # функции f и int. Вызов функции сопрограммы func() создает сопрограмму, которая должна быть
    # вычислена с помощью await.
    # Обратите внимание, что внутри спискового включения использование await не имеет никакого
    # отношения к использованию async for: они делают совершенно разные вещи и действуют на
    # совершенно разные объекты.
    results = [await func(x) async for func, x in factory(3)]
    print('results = ', results)


if __name__ == '__main__':
    asyncio.run(main())
    # results =  [100, 101, 102]
