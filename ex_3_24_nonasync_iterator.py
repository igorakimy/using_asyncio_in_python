class A:

    # Итератор должен реализовывать специальный метод __iter__().
    def __iter__(self):
        # Инициализация некого "начального" состояния.
        self.x = 0
        # Специальный метод __iter__() должен возвращать итерируемый объект, т.е. объект,
        # который реализует специальный метод __next__(). В данном случае это один и тот
        # же экземпляр, потому что A сам также реализует специальный метод __next__().
        return self

    # Определен метод __next__(). Он будет вызываться для каждого шага в последовательности
    # итераций до тех пор, пока...
    def __next__(self):
        if self.x > 2:
            # ...не будет выброшено исключение StopIteration.
            raise StopIteration
        self.x += 1
        # Генерируются возвращаемые значения для каждой итерации.
        return self.x


if __name__ == '__main__':
    for i in A():
        print(i)
    # 1
    # 2
    # 3