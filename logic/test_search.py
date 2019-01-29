# -*- coding: utf-8 -*-

import unittest
from agents import *
from logic import *
from utils import *
from search import *

class TestSearch(unittest.TestCase):
    def test_PlanRoute(self):
        initial = WumpusPosition(1,2,'LEFT')
        goals = (4,2)
        allowed = []
        for position in [[i, j] for i in range(1,5) for j in range(1,5)]:
            allowed.append(position)
        for forbidden in [[i,j] for i in range(2,4) for j in range(2,4)]:
            allowed.remove(forbidden)
        problem = PlanRoute(initial, goals, allowed, 4)
        solutions = astar_search(problem).solution()
        print("solution is ", solutions)

if __name__ == '__main__':
    unittest.main()
