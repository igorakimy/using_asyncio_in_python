import asyncio


async def f():
    await asyncio.sleep(1.0)
    return 123


async def main():
    # Вызов f() создает сопрограмму; это означает, что нам разрешено ее ожидать при помощи
    # ключевого слова await. Значение переменной result будет равно 123, когда f() завершится.
    result = await f()
    return result


if __name__ == '__main__':
    res = asyncio.run(main())
    print(res)
    # 123
