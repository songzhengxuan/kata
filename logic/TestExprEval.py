import collections


class Expr(object):
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def __add__(self, rhs):
        return Expr('+', self, rhs)
    
    def __mul__(self, rhs):
        return Expr('*', self, rhs)
    
    def __rmul__(self, lhs):
        return Expr('*', lhs, self)

    def __repr__(self):
        op = self.op
        args = [str(arg) for arg in self.args]
        if op.isidentifier():
            return '{}({})'.format(op, ', '.join(args)) if args else ("." + str(op))
        elif len(args) == 1:
            return op + args[0]
        else:
            opp = (' ' + op + ' ')
            return '(' + opp.join(args) + ')'


def Symbol(name):
    return Expr(name)


def expr(x):
    if isinstance(x, str):
        return eval(x, defaultkeydict(Symbol))
    else:
        return x


class defaultkeydict(collections.defaultdict):
    def __missing__(self, key):
        self[key] = result = self.default_factory(key)
        return result


def main():
    print("use this in command line")


if __name__ == "__main__":
    main()
