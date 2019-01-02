from utils import Expr
from agents import Thing
import utils
import logic


class TestThing(Thing):
    def __init__(self, name):
        self.__name__ = name
        self.alive = False

    @property
    def get_name(self):
        return self.__name__

    @property
    def set_name(self, name):
        print("set called")
        self.__name__ = name


def testThing():
    th = TestThing("agent")
    print("thing is ", th)
    th.name = "abc"
    print("thing is ", th)
    print("thing is", th.is_alive())


def main():
    a = [i for i in range(10) if i % 2 == 1]
    b = [i for i in range(10, 16) if i % 2 == 1]
    print(a)
    print(b)
    c = [(i, j) for (i, j) in zip(a, b)]
    print(c)

    testThing()

    a = utils.expr('A & B')
    A = Expr('A')
    B = Expr('B')
    print(logic.pl_true(a, {A: True, B: True}))


if __name__ == "__main__":
    main()
