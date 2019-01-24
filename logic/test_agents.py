# -*- coding: utf-8 -*-

import unittest
from agents import *
from logic import *
from utils import *

# Useful constant Exprs used in examples and code:
A, B, C, D, E, F, G, P, Q, x, y, z = map(Expr, 'ABCDEFGPQxyz')


class TestEnvironment(unittest.TestCase):
    """Test mathfuc.py"""

    def test_add(self):
        """Test method add(a, b)"""
        self.assertEqual(2, 1+1)

    def test_buildEnv(self):
        """Test we can build an XYEnvironment"""
        env = XYEnvironment(10, 10)
        self.assertTrue(env is not None)
        self.assertEqual(10, env.width)
        self.assertEqual(10, env.height)

    def test_AddWalls(self):
        """Test after add walls, the XYEnvironment start and end changed"""
        env = XYEnvironment(10, 10)
        self.assertTrue(env is not None)
        self.assertEqual(10, env.width)
        self.assertEqual(10, env.height)
        env.add_walls()
        self.assertEqual(1, env.x_start)
        self.assertEqual(9, env.x_end)
        self.assertEqual(1, env.y_start)
        self.assertEqual(9, env.y_end)

    def test_AddThingsAndAgents(self):
        """Test after add things ,the environment will have the added thing"""
        env = XYEnvironment(10, 10)
        thing = Obstacle()
        env.add_thing(thing, (1, 3))
        agent = Agent()
        env.add_thing(agent, (1, 2))
        self.assertEqual(2, len(env.things))
        self.assertEqual(1, len(env.agents))
        nearthings = env.percept(agent)
        print(nearthings)


class TestExpr(unittest.TestCase):
    def test_cnfBase(self):
        self.assertTrue(expr('Q') == Expr('Q'))

        self.assertTrue(expr('A & B') == Expr('&', Expr('A'), Expr('B')))

    def test_move_not_inwards(self):
        self.assertEqual(move_not_inwards(~(A | B)), (~A & ~B))
        self.assertEqual(move_not_inwards(~(A & B)), (~A | ~B))
        self.assertEqual(move_not_inwards(~(~(A | ~B) | ~~C)), ((A | ~B) & ~C))

    def test_distribute_and_over_ors(self):
        a = (A & B) | C
        b = (A | C) & (B | C)
        self.assertEquals(distribute_and_over_or(a), b)

        a = ((A & B) | C) & D
        b = ((A | C) & (B | C)) & D
        self.assertEquals(distribute_and_over_or(a), b)

    def test_prop_symbols(self):
        a = (A & B) | C
        self.assertEquals(prop_symbols(a), {A, B, C})
        self.assertEquals(prop_symbols(a), {A, C, B})

    def test_tt_entails(self):
        a = (A & B)
        b = B
        self.assertTrue(tt_entails(a, b))

    def test_cnfOfSymbol(self):
        orig = expr('Q')
        self.assertTrue(to_cnf(orig) == Expr('Q'))
        orig = expr("~(A|B)")
        # self.assertTrue(to_cnf(orig) == expr("~A & ~B"))
        # self.assertTrue(repr(to_cnf("a | (b & c) | d")) == '((b | a | d) & (c | a | d))')


class TestKB(unittest.TestCase):
    def test_PropKB(self):
        kb = PropKB()
        self.assertTrue(count(kb.ask(expr) for expr in [A, C, D, E, Q]) is 0)
        kb.tell(A & E)
        self.assertTrue(kb.ask(D) == False)

        self.assertTrue(kb.ask(A) == kb.ask(E) == {})
        self.assertTrue(kb.ask(~A) == kb.ask(~E) == False)
        kb.tell(E | '==>' | C)
        self.assertTrue(kb.ask(C) == {})
        kb.retract(E)
        self.assertTrue(kb.ask(E) == False)
        self.assertTrue(kb.ask(C) == False)


class TestWumpus(unittest.TestCase):

    def test_InitEnvironment(self):
        env = WumpusEnvrionment(lambda percept: None)
        print("world is", env.get_world())
    
    def test_InitTestEnvironment(self):
        things = []
        w = Wumpus()
        w.location = (1,2)
        things.append(w)
        env = WumpusEnvrionmentForTest(lambda percept: None, 6, 6, things=things)
        print("test world is", env.get_world())
        agent = Explorer()
        agent.location = (1,1)
        percepts = env.percepts_from(agent, (1,1))
        print("percepts is ", percepts)
        self.assertTrue(len(percepts) > 1)

    def test_wumpus_example(self):
        wumpus_kb = PropKB()
        P11, P12, P21, P22, P31, B11, B21 = expr(
            'P11, P12, P21, P22, P31, B11, B21')
        wumpus_kb.tell(~P11)
        wumpus_kb.tell(B11 | '<=>' | ((P12 | P21)))
        wumpus_kb.tell(B21 | '<=>' | ((P11 | P22 | P31)))
        wumpus_kb.tell(~B11)
        wumpus_kb.tell(B21)
        # Statement: There is no pit in [1,1].
        self.assertTrue(wumpus_kb.ask(~P11) == {})

        # Statement: There is no pit in [1,2].
        self.assertTrue(wumpus_kb.ask(~P12) == {})

        # Statement: There is a pit in [2,2].
        self.assertTrue(wumpus_kb.ask(P22) is False)

        # Statement: There is a pit in [3,1].
        self.assertTrue(wumpus_kb.ask(P31) is False)

        # Statement: Neither [1,2] nor [2,1] contains a pit.
        self.assertTrue(wumpus_kb.ask(~P12 & ~P21) == {})

        # Statement: There is a pit in either [2,2] or [3,1].
        self.assertTrue(wumpus_kb.ask(P22 | P31) == {})


if __name__ == '__main__':
    unittest.main()
