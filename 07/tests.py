import unittest
import numpy as np

from multiply import multiply
from perf import pymultiply


class TestCAPI(unittest.TestCase):
    def test_multiply(self):
        A = np.random.randint(5, size=(60, 80))
        B = np.random.randint(2, size=(80, 50))
        a = A.tolist()
        b = B.tolist()

        self.assertEqual(multiply(a, b)[0:], np.dot(A, B).tolist()[0:])
        self.assertEqual(pymultiply(a, b)[0:], np.dot(A, B).tolist()[0:])
