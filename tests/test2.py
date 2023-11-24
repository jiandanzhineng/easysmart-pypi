import multiprocessing as mp
import os
import time


def f(f2):
    for i in range(10):
        time.sleep(0.1)
        f2()

def f3(f):
    f()


class A:
    def __init__(self):
        self.mac = os.urandom(6).hex()
        self.p = mp.Process(target=f, args=(self.f2,))
        self.p.start()

    def f(self):
        print(f'f is {self.mac}')

    def f2(self):
        print(f'f2 is {self.mac}')
        self.p = mp.Process(target=f3, args=(self.f,))
        self.p.start()

class B:
    def action1(self):
        ...

if __name__ == '__main__':
    a = B()
    res = hasattr(a, 'action1')
    print(res)
    print(dir(a))
