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
        a = expr('A <=> B')
        b = Expr('&', A |'==>'|B, B |'==>'|A)
        print("to_cnf a ", to_cnf(a))
        print("to_cnf b ", to_cnf(b))
        self.assertTrue(str(to_cnf(a)) == str(to_cnf(b)))
    
    def test_cnfEquiv(self):
        a = equiv(A, B|C)
        print("equiv string is ", to_cnf(a))

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
        self.assertEqual(prop_symbols(a), {A, B, C})
        self.assertEqual(prop_symbols(a), {A, C, B})
        a = location(1, 1, 0)
        print(prop_symbols(a))

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
    
    def test_kb(self):
        kb = WumpusKB(2)
        shouldFalse = kb.ask_if_true(location(2,1,0))
        self.assertFalse(shouldFalse)
        shouldTrue = kb.ask_if_true(location(1,1,0))       
        self.assertTrue(shouldTrue)
    
    def test_InitTestEnvironment(self):
        things = []
        w = Wumpus(lambda x: "")
        w.location = (1,2)
        things.append(w)
        env = WumpusEnvrionmentForTest(lambda percept: None, 6, 6, things=things)
        print("test world is", env.get_world())
        agent = Explorer(lambda x:"")
        agent.location = (1,1)
        percepts = env.percepts_from(agent, (1,1))
        print("percepts is ", percepts)
        self.assertTrue(len(percepts) >= 1)
    
    
    def test_death(self):
        things = []

        w = Wumpus(lambda x:"")
        w.location = (1,3)
        things.append(w)

        w2 = Wumpus(lambda x:"")
        w2.location = (2,1)
        things.append(w2)


        agent = HybridWumpusAgent(4)
        agent.location = (1,1)
        things.append(agent)

        self.assertTrue(isinstance(agent.execute, collections.Callable))
        print("execute type is ", agent.execute, isinstance(agent.execute, collections.Callable))
        env = WumpusEnvrionmentForTest(None, 6, 6, things=things)
        print("agent's kb is ")
        for c in agent.kb.clauses:
            print("\t", c)
        print("test world is") 
        print_world(env.get_world())
        self.assertFalse(env.is_done())
        env.step()
        print("after 1 step world is ")
        print("test world is") 
        print_world(env.get_world())
        self.assertFalse(env.is_done())
        env.step()
        print("after 2 step world is ")
        print("test world is") 
        print_world(env.get_world())
        self.assertTrue(env.is_done())
    
    def test_ok_to_move_judge(self):
        things = []

        w = Wumpus(lambda x:"")
        w.location = (3,1)
        things.append(w)

        agent = HybridWumpusAgent(4)
        agent.location = (1,1)
        things.append(agent)

        env = WumpusEnvrionmentForTest(None, 6, 6, things=things)
        self.assertTrue(agent.kb.ask(ok_to_move(1,2,0)) == {})
        print("kB is ", agent.kb)
    
    def test_not_ok_to_move(self):
        things = []

        w = Wumpus(lambda x:"")
        w.location = (2,1)
        things.append(w)
        
        agent = HybridWumpusAgent(4)
        agent.location = (1,1)
        things.append(agent)

        env = WumpusEnvrionmentForTest(None, 6, 6, things=things)
        percepts = env.percept(agent)
        print("percepts is ", percepts)
        agent.kb.add_temporal_sentences(0)
        isOkToMove = agent.kb.ask(ok_to_move(1,2,0))
        self.assertFalse(isOkToMove)
        print("kB is ", agent.kb.clauses)


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
