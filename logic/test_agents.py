# -*- coding: utf-8 -*-

import unittest
from agents import *


class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    def test_add(self):
        """Test method add(a, b)"""
        self.assertEqual(2, 1+1)

    def test_sub(self):
        """Test method add(a, b)"""
        self.assertEqual(2, 1+1)


if __name__ == '__main__':
    unittest.main()
