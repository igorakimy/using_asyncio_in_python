# Модуль inspect в стандартной библиотеке может обеспечить гораздо лучшие возможности для
# самоанализа, чем встроенная функция type.
import inspect


# Это самое простое из возможных объявлений сопрограммы: она выглядит как обычная функция,
# за исключением того, что начинается с ключевых слов async def.
async def f():
    return 123


if __name__ == '__main__':
    # Точный тип f - это не "сопрограмма"; это просто обычная функция. Хотя async def принято
    # назвать сопрограммами, строго говоря, Python рассматривает их как функции сопрограммы.
    # Это поведение идентично тому, как функции генератора работают в Python.
    print(type(f))
    # <class 'function'>

    # Существует функция iscoroutinefunction(), которая позволяет вам отличить обычную функцию
    # от функции сопрограммы.
    print(inspect.iscoroutinefunction(f))
    # True