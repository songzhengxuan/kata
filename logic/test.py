from utils import Expr
import utils
import logic


def test(a, b, **c):
    print(a)
    print(b)
    for k, v in c.items():
        print("{}:{}".format(k, v))


def main():
    a = utils.expr('A')
    A = Expr('A')
    print(logic.pl_true(a, {A: True}))


if __name__ == "__main__":
    main()
    test(1, 2, c=3)
