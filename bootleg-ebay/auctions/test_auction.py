import unittest
from unittest import TestCase


class TestAuction(TestCase):
    # TODO(jin): Write some more tests for auction
    def test_sum(self):
        
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()