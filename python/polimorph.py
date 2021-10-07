class A:
    def __init__(self):
        self.a = 'a'

    def method_a(self):
        print('self.a')

    a = 'dfdf'

class B:
    def __init__(self):
        self.b = 'b'

    def method_b(self):
        print('self.b')


class C(A, B):
    pass


c = C()

c.method_b()
c.method_a()


