from utils import Expr


def test(a, b, **c):
    print(a)
    print(b)
    for k, v in c.items():
        print("{}:{}".format(k, v))


def main():
    a = Expr('|', "hello", "world")
    print(a)


if __name__ == "__main__":
    main()
    test(1, 2, c=3)
