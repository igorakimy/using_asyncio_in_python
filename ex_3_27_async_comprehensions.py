import asyncio


async def doubler(n):
    for i in range(n):
        # doubler() - это очень простой асинхронный генератор: при заданном верхнем значении
        # он выполняет итерацию по простому диапазону, получая кортеж значения и его удвоение.
        yield i, i * 2
        # Немного поспать, просто, чтобы подчеркнуть, что это действительно асинхронная функция.
        await asyncio.sleep(.1)


async def main():
    # Асинхронное списковое включение: обратите внимание, как используется async for вместо
    # обычного for.
    result = [x async for x in doubler(3)]
    print(result)
    # Асинхронное словарное включение; работают все обычные приемы, такие как распаковка кортежа
    # в 'x' и 'y', чтобы они могли передавать синтаксис словарного включения.
    result = {x: y async for x, y in doubler(3)}
    print(result)
    # Асинхронное множественное включение работает так же, как и ожидалось.
    result = {x async for x in doubler(3)}
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
    # [(0, 0), (1, 2), (2, 4)]
    # {0: 0, 1: 2, 2: 4}
    # {(2, 4), (1, 2), (0, 0)}
