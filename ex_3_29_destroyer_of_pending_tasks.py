import asyncio


async def f(delay):
    await asyncio.sleep(delay)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Задача 1 будет выполняться в течение 1 секунды.
    t1 = loop.create_task(f(1))
    # Задача 2 будет выполняться в течение 2 секунд.
    t2 = loop.create_task(f(2))
    # Запускать только до тех пор, пока задача 1 не будет завешена.
    loop.run_until_complete(t1)
    loop.close()
    # Task was destroyed but it is pending!
    # task: <Task pending name='Task-2' coro=<f() running at
    #   <stdin>:5> wait_for=<Future pending cb=[Task.task_wakeup()]>>
