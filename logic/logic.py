from utils import (
    first, Expr, expr, subexpressions
)

from agents import *

class KB:

    """A knowledge base to which you can tell and ask sentences.
    To create a KB, first subclass this class and implement
    tell, ask_generator, and retract.  Why ask_generator instead of ask?
    The book is a bit vague on what ask means --
    For a Propositional Logic KB, ask(P & Q) returns True or False, but for an
    FOL KB, something like ask(Brother(x, y)) might return many substitutions
    such as {x: Cain, y: Abel}, {x: Abel, y: Cain}, {x: George, y: Jeb}, etc.
    So ask_generator generates these one at a time, and ask either returns the
    first one or returns False."""

    def __init__(self, sentence=None):
        raise NotImplementedError

    def tell(self, sentence):
        """Add the sentence to the KB"""
        raise NotImplementedError

    def ask(self, query):
        """Return a substitution that makes the query true, or, failing that, return False."""
        return first(self.ask_generator(query), default=False)

    def ask_generator(self, query):
        """Yield all the substitutions that make query true."""
        raise NotImplementedError

    def retract(self, sentence):
        """remove sentence from the KB."""
        raise NotImplementedError


class PropKB(KB):
    """A KB for propositional logic. Inefficinent, with no indexing. """

    def __init__(self, sentence=None):
        self.clauses = []
        if sentence:
            self.tell(sentence)

    def tell(self, sentence):
        """Add the sentence's clauses to the KB."""
        self.clauses.extend(conjuncts(to_cnf(sentence)))

    def ask_generator(self, query):
        """yeild the empty substituion{} if KB entails query; else not results."""
        if tt_entails(Expr('&', *self.clauses), query):
            yield {}

    def ask_if_true(self, query):
        """Return True is the KB entails query, else return False."""
        for _ in self.ask_generator(query):
            return True
        return False

    def retract(self, sentence):
        """Remove the sentence's clauses from the KB."""
        for c in conjuncts(to_cnf(sentence)):
            if c in self.clauses:
                self.clauses.remove(c)


def is_symbol(s):
    """A string s is a symbol if it starts with an aplphabetic char.
    >>> is_symbol('R2D2')
    True
    """
    return isinstance(s, str) and s[:1].isalpha()


def is_var_symbols(s):
    """A logic variable symbol is an initial-lowercase strings.
    >>> is_var_symbol('EXE')
    False
    """
    return is_symbol(s) and s[0].islower()


def is_prop_symbol(s):
    """A proposition logic symbol is an intial-uppercase string.
    >>> is_prop_symbol('exe')
    False
    """
    return is_symbol(s) and s[0].isupper()


def pl_true(exp, model={}):
    """Return True if the propositional logic expression is true in the model,
    and False if it is false. If the model does not specify the value for
    every proposition, this may return None to indicate 'not obvious';
    this may happen even when the expression is tautological.
    >>> pl_true(P, {}) is None
    True
    """
    if exp in (True, False):
        return exp
    op, args = exp.op, exp.args
    if is_prop_symbol(op):
        return model.get(exp)
    elif op == '~':
        p = pl_true(args[0], model)
        if p is None:
            return None
        else:
            return not p
    elif op == '|':
        result = False
        for arg in args:
            p = pl_true(arg, model)
            if p is True:
                return True
            if p is None:
                result = None
        return result
    elif op == '&':
        result = True
        for arg in args:
            p = pl_true(arg, model)
            if p is False:
                return False
            if p is None:
                result = None
        return result
    p, q = args
    if op == '==>':
        return pl_true(~p | q, model)
    elif op == '<==':
        return pl_true(p | ~q, model)
    pt = pl_true(p, model)
    if pt is None:
        return None
    qt = pl_true(q, model)
    if qt is None:
        return None
    if op == '<=>':
        return pt == qt
    elif op == '^':
        return pt != qt
    else:
        raise ValueError("illegal operator in logic expression" + str(exp))


def to_cnf(s):
    """Convert a propositional logical sentence to conjuntive normal form.
    That is, to the form((A | ~B)...) & (B | C | ...) & ...)[p. 253]
    >>> to_cnf('~(B|C)')
    (~B & ~C)
    """
    s = expr(s)
    if isinstance(s, str):
        s = expr(s)
    s = eliminate_implications(s)  # Step 1, 2
    s = move_not_inwards(s)  # Step 3
    return distribute_and_over_or(s)  # Step 4


def eliminate_implications(s):
    """Change implications into equivalent form with only &, |, and ~,
    as logical operators."""
    s = expr(s)
    if not s.args or is_symbol(s.op):
        return s  # Atoms are unchanged.
    args = list(map(eliminate_implications, s.args))
    a, b = args[0], args[-1]
    if s.op == '==>':
        return b | ~a
    elif s.op == '<==':
        return a | ~b
    elif s.op == '<=>':
        return (b | ~a) & (a | ~b)
    elif s.op == '^':
        assert len(args) == 2  # TODO: relax this restrication
        return (a & ~b) | (~a & b)
    else:
        assert s.op in ('&', '|', '~')
        return Expr(s.op, *args)


def move_not_inwards(s):
    """Rewrite sentence s by moving negation sign inward.
    >>> move_not_inwards(~(A | B))
    (~A & ~B)
    """
    s = expr(s)
    if s.op == '~':
        def NOT(b):
            return move_not_inwards(~b)
        a = s.args[0]
        if a.op == '~':
            return move_not_inwards(a.args[0])  # ~~A ==> A
        if a.op == '&':
            return Expr('|', *list(map(NOT, a.args)))
        if a.op == '|':
            return Expr('&', *list(map(NOT, a.args)))
        return s
    elif is_symbol(s.op) or not s.args:
        return s
    else:
        return Expr(s.op, *list(map(move_not_inwards, s.args)))


def distribute_and_over_or(s):
    """Given a sentence s consisting of conjunctions and disjunctions
    of literals, return an equivalent sentence in CNF.
    >>> distribute_and_over_or((A & B) | C)
    ((A | B) & (B | C))
    """
    s = expr(s)
    if not isinstance(s, Expr):
        return s
    #firstParseArgs = tuple([distribute_and_over_or(arg) for arg in s.args])
    #s = Expr(s.op, firstParseArgs)
    if s.op == '|':
        for subarg in s.args:
            if subarg.op == '&':
                otherArgs = [
                    otherArg for otherArg in s.args if otherArg != subarg]

                newArgs = []
                if len(otherArgs) > 1:
                    otherExpr = Expr('|', tuple(otherArgs))
                    for t in subarg.args:
                        newArgs.append(Expr('|', t, otherExpr))
                else:
                    otherExpr = otherArgs[0]
                    for t in subarg.args:
                        newArgs.append(Expr('|', t, otherExpr))

                print("newArgs is ", newArgs)
                toReturn = Expr('&')
                toReturn.args = tuple(newArgs)
                print("toReturn is ", toReturn)
                return toReturn
    else:
        newArgs = []
        for subarg in s.args:
            newArgs.append(distribute_and_over_or(subarg))
        s.args = tuple(newArgs)
    return s


def associate(op, args):
    """Given an associative op, return an expression with the same
    meaning as Expr(op, *args), but flattened -- that is, with nested
    instances of the same op promoted to the top level.
    >>> associate('&', [(A&B),(B|C),(B&C)])
    (A & B & (B | C) & B & C)
    >>> associate('|', [A|(B|(C|(A&B)))])
    (A | B | C | (A & B))
    """
    args = dissociate(op, args)
    if len(args) == 0:
        return _op_identity[op]
    elif len(args) == 1:
        return args[0]
    else:
        return Expr(op, *args)


_op_identity = {'&': True, '|': False, '+': 0, '*': 1}


def dissociate(op, args):
    """Given an associative op, return a flattened list result such
    that Expr(op, *result) means the same as Expr(op, *args).
    >>> dissociate('&', [A & B])
    [A, B]
    """
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.op == op:
                collect(arg.args)
            else:
                result.append(arg)
    collect(args)
    return result


def conjuncts(s):
    """Return a list of conjuncts in sentence s
    >>>conjuncts(A & B)
    [A, B]
    >>>conjucts(A | B)
    [(A|B)]
    """
    return dissociate('&', [s])


def implies(lhs, rhs):
    return Expr('==>', lhs, rhs)


def equiv(lhs, rhs):
    return Expr('<=>', lhs, rhs)


def new_disjunction(sentences):
    t = sentences[0]
    for i in range(1, len(sentences)):
        t |= sentences[i]
    return t


def variables(s):
    """Return a set of the variables in expression s.
    >>> variables(expor('F(x,x) & G(x,y) & H(y, z) & R(A,z,2)')) == {x,y,z}
    True
    """
    return {x for x in subexpressions(s) if is_variable(x)}


def is_variable(x):
    """A variable is an Expr with no args and a lowercase symbol as the op."""
    return isinstance(x, Expr) and not x.args and x.op[0].islower()


def tt_entails(kb, alpha):
    """Does kb entail the sentence alpha? Use truth tables. For propositional
    kb's and sentences.[Figure 7.10]. Note that the 'kb' should be an
    Expr which is a conjunction of clauses.
    >>> tt_entails(expr('P & Q'), expr('Q'))
    True
    """
    model = {}
    symbols = list(prop_symbols(kb & alpha))
    return tt_check_all(kb, alpha, symbols, model)


def tt_check_all(kb, alpha, symbols, model):
    if not symbols:
        if pl_true(kb, model):
            return pl_true(alpha, model)
        else:
            return True
    else:
        p, reset = symbols[0], symbols[1:]
        return tt_check_all(kb, alpha, reset, extends(model, p, True))and tt_check_all(kb, alpha, reset, extends(model, p, False))


def extends(s, var, value):
    """Copy the substitution s and extend it by setting var to val; return copy.
    >>> extend({x: 1}, y, 2) == {x: 1, y: 2}
    True
    """
    s2 = s.copy()
    s2[var] = value
    return s2


def prop_symbols(x):
    """Return the set of all propositional symbols in x."""
    if not isinstance(x, Expr):
        return set()
    if is_prop_symbol(x.op) and not x.args:
        return {x}
    else:
        return {symbol for arg in x.args for symbol in prop_symbols(arg)}

def facing_east(time):
    return Expr('FacingEast', time)

def facing_west (time):
    return Expr('FacingWest', time)

def facing_north (time):
    return Expr('FacingNorth', time)

def facing_south (time):
    return Expr('FacingSouth', time)

def wumpus (x, y):
    return Expr('W', x, y)

def pit(x, y):
    return Expr('P', x, y)

def breeze(x, y):
    return Expr('B', x, y)

def stench(x, y):
    return Expr('S', x, y)

def wumpus_alive(time):
    return Expr('WumpusAlive', time)

def have_arrow(time):
    return Expr('HaveArrow', time)

def percept_stench(time):
    return Expr('Stench', time)

def percept_breeze(time):
    return Expr('Breeze', time)

def percept_glitter(time):
    return Expr('Glitter', time)

def percept_bump(time):
    return Expr('Bump', time)

def percept_scream(time):
    return Expr('Scream', time)

def move_forward(time):
    return Expr('Forward', time)

def shoot(time):
    return Expr('Shoot', time)

def turn_left(time):
    return Expr('TurnLeft', time)

def turn_right(time):
    return Expr('TurnRight', time)

def ok_to_move(x, y, time):
    return Expr('OK', x, y, time)

def location(x, y, time = None):
    if time is None:
        return Expr('L', x, y)
    else:
        return Expr('L', x, y, time)

class WumpusKB(PropKB):
    """Create a Knowledge Base that contains the atemporal "Wumpus physics" and temporal rules with time zero."""

    def __init__(self, dimrow):
        super().__init__()
        self.dimrow = dimrow
        self.tell(~wumpus(1, 1))
        self.tell(~pit(1, 1))

        for y in range(1, dimrow + 1):
            for x in range(1, dimrow + 1):
                pits_in = list()
                wumpus_in = list()

                if x > 1:
                    pits_in.append(pit(x - 1, y))
                    wumpus_in.append(wumpus(x - 1, y))

                if y < dimrow:
                    pits_in.append(pit(x, y + 1))
                    wumpus_in.append(wumpus(x, y + 1))

                if x < dimrow:
                    pits_in.append(pit(x + 1, y))
                    wumpus_in.append(wumpus(x + 1, y))

                if y > 1:
                    pits_in.append(pit(x, y - 1))
                    pits_in.append(wumpus(x, y - 1))

                self.tell(equiv(breeze(x, y), new_disjunction(pits_in)))
                self.tell(equiv(stench(x, y), new_disjunction(wumpus_in)))

        ## Rule that describes existence of at least one Wumpus
        wumpus_at_least = list()
        for x in range(1, dimrow+1):
            for y in range(1, dimrow+1):
                wumpus_at_least.append(wumpus(x, y))
        
        self.tell(new_disjunction(wumpus_at_least))

        ## Rule that describes existence of at most one Wumpus
        for i in range(1, dimrow+1):
            for j in range(1, dimrow+1):
                for u in range(1, dimrow+1):
                    for v in range(1, dimrow+1):
                        if i!=u or j!=v:
                            self.tell(~wumpus(i, j) | ~wumpus(u, v))
        
        ## Temporal rules at time zero
        self.tell(location(1, 1, 0))
        for i in range(1, dimrow+1):
            for j in range(1, dimrow+1):
                self.tell(implies(location(i, j, 0), equiv(percept_breeze(0), breeze(i, j))))
                self.tell(implies(location(i, j, 0), equiv(percept_stench(0), stench(i, j))))
                if i != 1 or j != 1:
                    self.tell(~location(i, j, 0))
        
        self.tell(wumpus_alive(0))
        self.tell(have_arrow(0))
        self.tell(facing_east(0))
        self.tell(~facing_north(0))
        self.tell(~facing_south(0))
        self.tell(~facing_west(0))
    
    def make_action_sentence(self, action, time):
        actions = [move_forward(time), shoot(time), turn_right(time), turn_right(time)]

        for a in actions:
            if action is a:
                self.tell(action)
            else:
                self.tell(~a)
    
    def make_percept_sentence(self, percept, time):
        # Glitter, Bump, Stench, Breeze, Scream
        flags = [0, 0, 0, 0, 0]

        ## Things perceived
        if isinstance(percept, Glitter):
            flags[0] = 1
            self.tell(percept_glitter(time))
        elif isinstance(percept, Bump):
            flags[1] = 1
            self.tell(percept_bump(time))
        elif isinstance(percept, Stench):
            flags[2] = 1
            self.tell(percept_stench(time))
        elif isinstance(percept, Breeze):
            flags[3] = 1
            self.tell(percept_breeze(time))
        elif isinstance(percept, Scream):
            flags[4] = 1
            self.tell(percept_scream(time))
        
        ## Things not perceived
        for i in len(range(flags)):
            if flags[i] == 0:
                if i == 0:
                    self.tell(~percept_glitter(time))
                elif i == 1:
                    self.tell(~percept_bump(time))
                elif i == 2:
                    self.tell(~percept_stench(time))
                elif i == 3:
                    self.tell(~percept_breeze(time))
                elif i == 4:
                    self.tell(~percept_scream(time))
    
    def add_temporal_sentences(self, time):
        if time == 0:
            return 
        t = time - 1

        ## current location rules
        for i in range(1, self.dimrow+1):
            for j in range(1, self.dimrow+1):
                self.tell(implies(location(i, j, time), equiv(percept_breeze(time), breeze(i, j))))
                self.tell(implies(location(i, j, time), equiv(percept_stench(time), stench(i, j))))

                s = list()

                # the agent will stay in i, j after time if it not move in time
                s.append(
                    equiv(
                        location(i, j, time),
                        location(i, j, time) & ~move_forward(time) | percept_bump(time)
                    ))
                
                if i != 1:
                    s.append(location(i - 1, j, t) & facing_east(t) & move_forward(t))
                if i != self.dimrow:
                    s.append(location(i+1, j, t) & facing_west(t) & move_forward(t))
                if j != 1:
                    s.append(location(i, j - 1, t) & facing_north(t) & move_forward(t))
                if j != self.dimrow:
                    s.append(location(i, j + 1, t) & facing_south(t) & move_forward(t))
                
                ## add sentence about location i, j
                self.tell(new_disjunction(s))

                ## add sentence about safety of location i, j
                self.tell(
                    equiv(ok_to_move(i, j, time), ~pit(i, j) & ~wumpus(i, j) & wumpus_alive(time) )
                )

        ## Rules about current orientation

        a = facing_north(t) & turn_right(t)
        b = facing_south(t) & turn_left(t)
        c = facing_east(t) & ~turn_left(t) & ~turn_right(t)
        s = equiv(facing_east(time), a | b | c)
        self.tell(s)

        a = facing_north(t) & turn_left(t)
        b = facing_south(t) & turn_right(t)
        c = facing_west(t) & ~turn_left(t) & ~turn_right(t)
        s = equiv(facing_west(time), a | b | c)
        self.tell(s)

        a = facing_west(t) & turn_left(t)
        b = facing_east(t) & turn_right(t)
        c = facing_south(t) & ~turn_left(t) & ~turn_right(t)
        s = equiv(facing_south(time), a | b | c)
        self.tell(s)

        a = facing_west(t) & turn_right(t)
        b = facing_east(t) & turn_left(t)
        c = facing_north(t) & ~turn_left(t) & ~turn_right(t)
        s = equiv(facing_north(time), a | b | c)
        self.tell(s)

        ## Rules about last action
        self.tell(equiv(move_forward(t), ~turn_right(t) & ~turn_left(t)))

        ## Rules about the arrow
        self.tell(equiv(have_arrow(time), have_arrow(t) & ~shoot(t)))

        ## Rule about Wumpus (dead or alive)
        self.tell(equiv(wumpus_alive(time), wumpus_alive(t) & ~percept_scream(time)))
    
    def ask_if_true(self, query):
        return pl_true(self, query)


            

        
        
