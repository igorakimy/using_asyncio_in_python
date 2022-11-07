import asyncio
import time


async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


# blocking() вызывает традиционную функцию time.sleep() внутри, которая заблокировала бы поток
# и предотвратила запуск вашего цикла событий. Это означает, что вы не должны делать эту функцию
# сопрограммой - действительно, вы даже не можете вызвать эту функцию из любого места в главном
# потоке, где выполняется цикл asyncio. Мы решаем эту проблему, запуская эту функцию в
# исполнителе (отдельном потоке).
def blocking():
    time.sleep(0.5)
    print(f'{time.ctime()} Hello from blocking func!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    # await loop.run_in_executor(None, func)
    # Это последняя из нашего списка функций asyncio, которые необходимо знать. Иногда вам нужно
    # запускать что-то в отдельном потоке или даже отдельном процессе: этот метод используется
    # именно для этого. Здесь мы передаем нашу блокирующую функцию для запуска в исполнителе по
    # умолчанию. Обратите внимание, что run_in_executor() не блокирует основной поток: он только
    # планирует выполнение задачи исполнителем (он возвращает объект Future, а это означает, что
    # вы можете ожидать (await) его, если метод вызывается в рамках другой сопрограммы). Задача
    # исполнителя начнет выполняться только после того, как run_until_complete() будет вызываться,
    # что позволяет циклу событий начать обработку событий.
    loop.run_in_executor(None, blocking)
    loop.run_until_complete(task)

    # Набор задач в ожидании не включает сущность, вызывающую blocking(), которая была выполнена
    # в run_in_executor(). Это будет справедливо для любого вызова, который возвращает объект
    # Future, а не Task. all_tasks() в действительности возвращает только объекты Task, а не
    # Future.
    pending = asyncio.all_tasks(loop=loop)
    for task in pending:
        task.cancel()

    group = asyncio.gather(*pending, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()

    # Mon Nov  7 13:42:04 2022 Hello!
    # Mon Nov  7 13:42:04 2022 Hello from blocking func!
    # Mon Nov  7 13:42:05 2022 Goodbye!
