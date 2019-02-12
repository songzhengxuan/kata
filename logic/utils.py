import collections
import collections.abc
import math
import heapq
import functools

def removeall(item, seq):
    """Return a copy oof seq (or string) with all occurrences of tiem removed."""
    if isinstance(seq, str):
        return seq.replace(item, '')
    else:
        return [x for x in seq if x != item]

def unique(seq):  # TODO: replace with set
    """Remove duplicate elements from seq. Assumes hashable elements."""
    return list(set(seq))

def first(iterable, default=None):
    """return the firt element of an iterable or the next element of a generator; or default"""
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)


class Expr(object):
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    # Operator overloads
    def __neg__(self):
        return Expr('-', self)

    def __pos__(self):
        return Expr('+', self)

    def __invert__(self):
        return Expr('~', self)

    def __add__(self, rhs):
        return Expr('+', self, rhs)

    def __sub__(self, rhs):
        return Expr('-', self, rhs)

    def __mul__(self, rhs):
        return Expr('*', self, rhs)

    def __pow__(self, rhs):
        return Expr('**', self, rhs)

    def __mod__(self, rhs):
        return Expr('%', self, rhs)

    def __and__(self, rhs):
        return Expr('&', self, rhs)

    def __xor__(self, rhs):
        return Expr('^', self, rhs)

    def __rshift__(self, rhs):
        return Expr('>>', self, rhs)

    def __lshift__(self, rhs):
        return Expr('<<', self, rhs)

    def __truediv__(self, rhs):
        return Expr('/', self, rhs)

    def __floordiv__(self, rhs):
        return Expr('//', self, rhs)

    def __matmul__(self, rhs):
        return Expr('@', self, rhs)

    def __or__(self, rhs):
        if isinstance(rhs, Expression):
            return Expr('|', self, rhs)
        else:
            return PartialExpr(rhs, self)

    # Reverse operator overloads
    def __radd__(self, lhs):
        return Expr('+', lhs, self)

    def __rsub__(self, lhs):
        return Expr('-', lhs, self)

    def __rmul__(self, lhs):
        return Expr('*', lhs, self)

    def __rdiv__(self, lhs):
        return Expr('/', lhs, self)

    def __rpow__(self, lhs):
        return Expr('**', lhs, self)

    def __rmod__(self, lhs):
        return Expr('%', lhs, self)

    def __rand__(self, lhs):
        return Expr('&', lhs, self)

    def __rxor__(self, lhs):
        return Expr('^', lhs, self)

    def __ror__(self, lhs):
        return Expr('|', lhs, self)

    def __rrshift__(self, lhs):
        return Expr('>>', lhs, self)

    def __rlshift__(self, lhs):
        return Expr('<<', lhs, self)

    def __rtruediv__(self, lhs):
        return Expr('/', lhs, self)

    def __rfloordiv__(self, lhs):
        return Expr('//', lhs, self)

    def __rmatmul__(self, lhs):
        return Expr('@', lhs, self)

    def __call__(self, *args):
        "Call: if 'f' is a Symbol, then f(0) == Expr('f', 0)."
        if self.args:
            raise ValueError('can only do a call for a Symbol, not an Expr')
        else:
            return Expr(self.op, *args)

    #Equality and repr

    def __eq__(self, other):
        "'x == y' evaluates to True or False; does not build an Expr."
        return (isinstance(other, Expr)
                and self.op == other.op
                and self.args == other.args)

    def __hash__(self):
        return hash(self.op) ^ hash(self.args)

    def __repr__(self):
        op = self.op
        args = [str(arg) for arg in self.args]
        if op.isidentifier():  # f(x) for f(x, y)
            return '{}({})'.format(op, ', '.join(args)) if args else op
        elif len(args) == 1:
            return op + args[0]
        else:  # (x - y)
            opp = (' ' + op + ' ')
            return '(' + opp.join(args) + ')'

# For operators that are not defined in Python, we allow new InfixOps:


Number = (int, float, complex)
Expression = (Expr, Number)


def Symbol(name):
    """A Symbol is just an Expr with no args."""
    return Expr(name)


def symbols(names):
    """return a tumple of Symbols; names is a comma/whitespace delimited str."""
    return tuple(Symbol(name) for name in names.replace(',', ' ').split())


def subexpressions(x):
    """Yield the subexpressions of an Expression (including x itself)."""
    yield x
    if isinstance(x, Expr):
        for arg in x.args:
            yield from subexpressions(arg)


def arity(expression):
    """the number of sub-expressions in this expression."""
    if isinstance(expression, Expr):
        return len(expression.args)
    else:
        return 0


class PartialExpr:
    """Given 'P |'==>'| Q',  first form PatialExpr('==>', P), then combine with Q. """

    def __init__(self, op, lhs):
        self.op, self.lhs = op, lhs

    def __or__(self, rhs):
        return Expr(self.op, self.lhs, rhs)

    def __repr__(self):
        return "ParitialExpr('{}', {})".format(self.op, self.lhs)


def expr(x):
    """Shortcut to create an Expression. x is a str in which:
    - identifiers are automatically defined as Symbols.
    - ==> is treated as an infix |'==>'| as are <== and <=>
    If x is already an Expression, it is returned unchanged. Example:
    >>> expr('P & Q ==> Q')
    ((P & Q) ==> Q)
    """
    if isinstance(x, str):
        return eval(expr_handle_infix_ops(x), defaultkeydict(Symbol))
    else:
        return x


infix_ops = '==> <== <=>'.split()


def expr_handle_infix_ops(x):
    """Given a str , return a new str with ==> replaced by |'==>'|, etc.
    >>> expr_handle_infix_ops('p ==> Q')
    "p |'==>'| Q"
    """
    for op in infix_ops:
        x = x.replace(op, '|' + repr(op) + '|')
    return x


class defaultkeydict(collections.defaultdict):
    """Like defaultdict ,but the default_factory is a funciton of the key.
    >>> d = defaultkeydict(len); d['four']
    4
    """

    def __missing__(self, key):
        self[key] = result = self.default_factory(key)
        return result


orientations = EAST, NORTH, WEST, SOUTH = [(1, 0), (0, 1), (-1, 0), (0, -1)]
turns = LEFT, RIGHT = (+1, -1)


def turn_heading(heading, inc, headings=orientations):
    return headings[(headings.index(heading) + inc) % len(headings)]


def turn_right(heading):
    return turn_heading(heading, RIGHT)


def turn_left(heading):
    return turn_heading(heading, LEFT)


def distance(a, b):
    """The distance between two (x, y) points."""
    xA, yA = a
    xB, yB = b
    return math.hypot((xA - xB), (yA - yB))


def distance_squared(a, b):
    """The square of the distance between two(x,y) points."""
    xA, yA = a
    xB, yB = b
    return (xA - xB) ** 2 + (yA - yB) ** 2


def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)

def multimap(items):
    """Given (key, val) pairs, return {key:[val, ...],...}."""
    result = defaultdict(list)
    for (key, val) in items:
        result[key].append(val)
    return result

def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)



def product(numbers):
    """Reutnr the product of the numbers, e.g. product([2,3,10]) == 60"""
    result = 1
    for x in numbers:
        result *= x
    return result

def print_world(world):
    for row in world:
        print(row)

def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is sepcified, store result in that slot of first argument.
    If slot if false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)
    
    return memoized_fn

class PriorityQueue:
    """A Queue in with the minimum(or maximum) element (as deter mined by f and order)
    if returned first.
    If order is 'min', the item with minimum f(x) is returned first;
    if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order="min", f=lambda x:x):
        self.heap = []

        if order == 'min':
            self.f = f
        elif order == 'max': # now tiem with max f(x)
            self.f = lambda x: -f(x)
        else:
            raise ValueError("order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert tiem at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))
    
    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)
    
    def pop(self):
        """Pop and return the item (with min or max f(x) value
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')
    
    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)
    
    def __contains__(self, item):
        """Return True if tiem in PriorityQueue."""
        return (self.f(item), item) in self.heap
    
    def __getitem__(self, key):
        for _, item in self.heap:
            if item == key:
                return item
    
    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        self.heap.remove((self.f(key), key))
        heapq.heapify(self.heap)
    





