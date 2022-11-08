from asyncio import Future


if __name__ == '__main__':
    f = Future()
    print(f.done())
    # False
