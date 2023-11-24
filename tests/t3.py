import asyncio

class A:
    p = 0

    async def f1(self):
        while True:
            print(f'f1:{self.p}')
            await asyncio.sleep(1)

    async def f2(self):
        while True:
            self.p += 1
            print(f'f2:{self.p}')
            await asyncio.sleep(1)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.f1())
        loop.create_task(self.f2())
        loop.run_forever()


if __name__ == '__main__':
    a = A()
    a.start()
