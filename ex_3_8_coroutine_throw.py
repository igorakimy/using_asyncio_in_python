async def f():
    return 123


if __name__ == '__main__':
    # Как и прежде, новая сопрограмма создается из функции сопрограммы f().
    coro = f()

    # Вместо того чтобы выполнять другую функцию send(), мы вызываем throw() и предоставляем класс
    # исключения и значение. Это вызывает исключение внутри нашей сопрограммы в точке await.
    coro.throw(Exception, 'blah')
    # Traceback (most recent call last):
    #   File "<stdin>", line 9, in <module>
    #     coro.throw(Exception, 'blah')
    #   File "<stdin>", line 1, in f
    #     async def f():
    # Exception: blah
