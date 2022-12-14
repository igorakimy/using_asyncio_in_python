import sys
import threading
from queue import Queue
from attr import attrs, attrib


# attrs, является библиотекой Python с открытым исходным кодом, которая ничего не
# предпринимает по отношению к потокам или asyncio, и является на самом деле восхитительной
# библиотекой для того, чтобы сделать создание класса простым. В нашем случае соответствующий
# декоратор @attrs гарантирует, что данный класс Cutlery получит весь обычный стереотипный
# код (подобный __init__()) автоматически установленным.
@attrs
class Cutlery:
    # Функция attrib предоставляет некий простой способ создания атрибутов, в том числе
    # значений по умолчанию, которые вы можете обычно обрабатывать как аргументы с ключевыми
    # словами в своем методе __init__().
    knives = attrib(default=0)
    forks = attrib(default=0)

    # Этот метод применяется для передачи ножей и вилок из одного объекта Cutlery в другой.
    # Обычно он применяется ботами для получения столовых приборов со своей кухни для новых
    # столов, а также для возврата этих столовых приборов обратно на кухню после уборки
    # данного стола.
    def give(self, to: 'Cutlery', knives: int = 0, forks: int = 0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    # Это очень простая функция утилиты для замены имеющихся инвентарных данных в данном
    # экземпляре объекта.
    def change(self, knives: int, forks: int):
        self.knives += knives
        self.forks += forks


# Мы определили kitchen в виде определенного идентификатора для конкретной кухонной
# инвентаризации столовых приборов. Обычно каждый из ботов будет получать столовые приборы
# в этом месте. Также необходимо чтобы они возвращали столовые приборы в это хранилище
# после уборки стола.
kitchen = Cutlery(knives=100, forks=100)


# ThreadBot является подклассом потока.
class ThreadBot(threading.Thread):

    def __init__(self):
        # Целевой функцией данного потока является метод manage_table, определяемый ниже.
        super().__init__(target=self.manage_table)
        # Этот бот собирается быть официантом и будет отвечать за некие столовые приборы.
        # Здесь все боты отслеживают те столовые приборы, которые они взяли со своей кухни.
        self.cutlery = Cutlery(knives=0, forks=0)
        # Конкретному боту также назначаются задачи. Они будут добавляться в данную очередь
        # задач, а сам бот будет исполнять их далее в своём основном цикле обработки.
        self.tasks = Queue()

    def manage_table(self):
        # Самой основной процедурой данного бота является данный бесконечный цикл. Если вам
        # потребуется остановить некоего бота, вам придется выдать ему задание "shutdown".
        while True:
            task = self.tasks.get()
            # Имеются только три задачи, определенные для данного бота. Самой первой,
            # "prepare table", является та, которую нужно выполнить, чтобы получить новый
            # стол готовым к обслуживанию. Для нашей проверки единственным требованием
            # является получить набор столовых приборов с кухни и поместить их на данный
            # стол. "clear table" служит для того, чтобы указать необходимость очистить
            # некий стол: данный бот должен вернуть использованные столовые приборы обратно
            # на кухню. "shutdown" всего лишь останавливает данного бота.
            if task == 'prepare table':
                kitchen.give(to=self.cutlery, knives=4, forks=4)
            elif task == 'clear table':
                self.cutlery.give(to=kitchen, knives=4, forks=4)
            elif task == 'shutdown':
                return


if __name__ == '__main__':
    # Этот сценарий исполняется при проверке. Для нашей проверки мы будем применять 10
    # Серийных ботов (threadbots).
    bots = [ThreadBot() for i in range(10)]

    for bot in bots:
        # Мы получаем общее число столов в виде параметра командной строки, а затем задаем
        # для каждого бота такое число задач для подготовки и уборки столов в своем ресторане.
        for i in range(int(sys.argv[1])):
            bot.tasks.put('prepare table')
            bot.tasks.put('clear table')
        # Задача "shutdown" заставит бота остановиться (так что bot.join() будет выполнять
        # возврат немного дальше). Оставшийся сценарий выводит диагностические сообщения и
        # запускает имеющихся ботов.
        bot.tasks.put('shutdown')

    print('Kitchen inventory before service: ', kitchen)

    for bot in bots:
        bot.start()

    for bot in bots:
        bot.join()

    print('Kitchen inventory after service: ', kitchen)
