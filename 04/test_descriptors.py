import unittest

from descriptors import IntAverage, String, PositiveInteger


class TestCustomMeta(unittest.TestCase):
    def setUp(self):
        class Data:  # pylint: disable=too-few-public-methods
            avg = IntAverage()
            name = String()
            price = PositiveInteger()

            def __init__(self, avg, name, price):
                self.avg = avg
                self.name = name
                self.price = price

        self.data = Data
        return super().setUp()

    def test_avg(self):
        data = self.data([0], "PC", 100)

        self.assertEqual(data.avg, 0)

        data.avg = [1, 2, 3]
        self.assertEqual(data.avg, 2)

        data.avg = [0, 1, 2, 3, 4, 5]

        with self.assertRaises(ValueError):
            data.avg = 0
        self.assertEqual(data.avg, 2.5)

        with self.assertRaises(ValueError):
            data.avg = "1234"
        self.assertEqual(data.avg, 2.5)

        with self.assertRaises(ValueError):
            data.avg = [1, 2, 2.1, 4]
        self.assertEqual(data.avg, 2.5)

        data.avg = []
        with self.assertRaises(ZeroDivisionError):
            data.avg  # pylint: disable=pointless-statement

    def test_name(self):
        data = self.data([0], "PC", 100)

        self.assertEqual(data.name, "PC")

        data.name = ""
        self.assertEqual(data.name, "")

        data.name = "746534211"
        self.assertEqual(data.name, "746534211")

        with self.assertRaises(ValueError):
            data.name = 0
        self.assertEqual(data.name, "746534211")

        with self.assertRaises(ValueError):
            data.name = [1, 2, 3]
        self.assertEqual(data.name, "746534211")

    def test_price(self):
        data = self.data([0], "PC", 100)

        self.assertEqual(data.price, 100)

        data.price = 1
        self.assertEqual(data.price, 1)

        data.price = 12345
        self.assertEqual(data.price, 12345)

        with self.assertRaises(ValueError):
            data.price = -1
        self.assertEqual(data.price, 12345)

        with self.assertRaises(ValueError):
            data.price = 0
        self.assertEqual(data.price, 12345)

        with self.assertRaises(ValueError):
            data.price = "100"
        self.assertEqual(data.price, 12345)


if __name__ == "__main__":
    unittest.main()
