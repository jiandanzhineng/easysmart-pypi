class A:
    p = 1

    def __init__(self):
        pass

    def display(self):
        print(self.p)

a = A()
a.display()
B = A
B.p = 3
b = B()
b.display()
