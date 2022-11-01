import unittest
import numpy as np

from multiply import multiply
from perf import pymultiply


class TestCAPI(unittest.TestCase):
    def test_matrix_shapes(self):
        A = []
        B = [[1, 2], [3, 4]]

        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "Matrix should not be a empty.",
        )

        A = [[1, 2], [3, 4]]
        B = []

        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "Matrix should not be a empty.",
        )

        A = [1]
        B = [[1, 2], [3, 4]]
        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "Non-list type found in list of lists.",
        )

        A = [[1, 2], [3, 4]]
        B = [1]
        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "Non-list type found in list of lists.",
        )

        A = [[]]
        B = [[]]

        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "ERROR: matrices should look like (m, n) and (n, l)",
        )

        A = [[1, 2, 3]]
        B = [[1, 2, 3]]

        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "ERROR: matrices should look like (m, n) and (n, l)",
        )

        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        B = [[1, 2, 3], [4, 6], [7, 8, 9]]

        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "Matrix should not be with variable row size.",
        )

        A = [[1, 2, 3], [4, 5, 6], [7, 9]]
        B = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        with self.assertRaises(RuntimeError) as manager:
            multiply(A, B)

        self.assertEqual(
            str(manager.exception),
            "Matrix should not be with variable row size.",
        )

    def test_multiply(self):
        A = np.random.randint(5, size=(60, 80))
        B = np.random.randint(2, size=(80, 50))
        a = A.tolist()
        b = B.tolist()

        self.assertEqual(multiply(a, b)[0:], np.dot(A, B).tolist()[0:])
        self.assertEqual(pymultiply(a, b)[0:], np.dot(A, B).tolist()[0:])
