"""Simple example test file.

See here: https://realpython.com/python-testing/ for how to write tests

"""

import unittest
from unittest import TestCase


class TestExample(TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()