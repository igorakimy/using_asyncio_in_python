import asyncio, time


async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


if __name__ == '__main__':
    asyncio.run(main())
    # Mon Nov  7 12:16:56 2022 Hello!
    # Mon Nov  7 12:16:57 2022 Goodbye!
