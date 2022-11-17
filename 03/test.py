import unittest

from CustomList import CustomList


class TestCustomList(unittest.TestCase):
    def test_list_methods(self):
        custom_list = CustomList([])
        custom_list.append(1)
        self.assertListEqual(custom_list, CustomList([1]))

        custom_list = CustomList([1, 2, 3])
        custom_list2 = custom_list.copy()
        self.assertListEqual(custom_list2, CustomList([1, 2, 3]))

        custom_list2.clear()
        self.assertListEqual(custom_list2, [])
        self.assertListEqual(custom_list, CustomList([1, 2, 3]))

        custom_list = CustomList([1, 2, 3, 2, 4, 2, 6, 4])
        self.assertEqual(custom_list.count(2), 3)
        self.assertEqual(custom_list.index(4), 4)

        custom_list = CustomList([1, 2, 3, 2, 4])
        custom_list.extend([1, 2])
        self.assertListEqual(
            custom_list,
            CustomList([1, 2, 3, 2, 4, 1, 2]),
        )

        custom_list = CustomList([1, 2, 3, 6, 4])
        custom_list.remove(6)
        self.assertListEqual(
            custom_list,
            CustomList([1, 2, 3, 4]),
        )

        custom_list = CustomList([1, 2, 3, 6, 4])
        custom_list.pop(2)
        self.assertListEqual(
            custom_list,
            CustomList([1, 2, 6, 4]),
        )

        custom_list = CustomList([1, 2, 3, 6, 4])
        custom_list.insert(3, 121)
        self.assertListEqual(
            custom_list,
            CustomList([1, 2, 3, 121, 6, 4]),
        )

        custom_list = CustomList([1, 23, 4, 21.4, -3])
        custom_list.reverse()
        self.assertListEqual(
            custom_list,
            CustomList([-3, 21.4, 4, 23, 1]),
        )

        custom_list.sort()
        self.assertListEqual(
            custom_list,
            CustomList([-3, 1, 4, 21.4, 23]),
        )

        custom_list.sort(reverse=True)
        self.assertListEqual(
            custom_list,
            CustomList([23, 21.4, 4, 1, -3]),
        )

    def test_addition(self):
        custom_list1 = CustomList([])
        custom_list2 = CustomList([])
        custom_list3 = CustomList([])
        self.assertListEqual(custom_list1 + custom_list2, custom_list3)
        self.assertListEqual(custom_list1, CustomList([]))
        self.assertListEqual(custom_list2, CustomList([]))

        custom_list1 = CustomList([1, 2])
        custom_list2 = CustomList([])
        custom_list3 = CustomList([1, 2])
        self.assertListEqual((custom_list1 + custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 2]))
        self.assertListEqual(custom_list2, CustomList([]))

        custom_list1 = CustomList([])
        custom_list2 = CustomList([3, 4])
        custom_list3 = CustomList([3, 4])
        self.assertListEqual((custom_list1 + custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([]))
        self.assertListEqual(custom_list2, CustomList([3, 4]))

        custom_list1 = CustomList([1, 2, 3, 4])
        custom_list2 = CustomList([1, 9])
        custom_list3 = CustomList([2, 11, 3, 4])
        self.assertListEqual((custom_list1 + custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 2, 3, 4]))
        self.assertListEqual(custom_list2, CustomList([1, 9]))

        custom_list1 = CustomList([1, 9])
        custom_list2 = CustomList([1, 2, 3, 4])
        custom_list3 = CustomList([2, 11, 3, 4])
        self.assertListEqual((custom_list1 + custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 9]))
        self.assertListEqual(custom_list2, CustomList([1, 2, 3, 4]))

        custom_list1 = CustomList([1, 9, 3, 10])
        custom_list2 = CustomList([1, -2, 3, -4])
        custom_list3 = CustomList([2, 7, 6, 6])
        self.assertListEqual((custom_list1 + custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 9, 3, 10]))
        self.assertListEqual(custom_list2, CustomList([1, -2, 3, -4]))

        custom_list1 = CustomList([1, 9, 3, 10])
        custom_list2 = CustomList([1, -2, 7, -4])
        custom_list1 += custom_list2
        custom_list3 = CustomList([2, 7, 10, 6])
        self.assertListEqual(custom_list1, custom_list3)
        self.assertListEqual(custom_list2, CustomList([1, -2, 7, -4]))

        custom_list1 = CustomList([1, 9, 3, 10])
        list2 = [1, -2, 1.2, -4]
        custom_list3 = CustomList([2, 7, 4.2, 6])
        self.assertListEqual((custom_list1 + list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 9, 3, 10]))
        self.assertListEqual(list2, [1, -2, 1.2, -4])

        list1 = [1, 9, 3, 10]
        custom_list2 = CustomList([1, -2, 3, -3.7])
        custom_list3 = CustomList([2, 7, 6, 6.3])
        self.assertListEqual((list1 + custom_list2), custom_list3)
        self.assertListEqual(list1, [1, 9, 3, 10])
        self.assertListEqual(custom_list2, CustomList([1, -2, 3, -3.7]))

    def test_subtraction(self):
        custom_list1 = CustomList([])
        custom_list2 = CustomList([])
        custom_list3 = CustomList([])
        self.assertListEqual(custom_list1 - custom_list2, custom_list3)
        self.assertListEqual(custom_list1, CustomList([]))
        self.assertListEqual(custom_list2, CustomList([]))

        custom_list1 = CustomList([1, 2])
        custom_list2 = CustomList([])
        custom_list3 = CustomList([1, 2])
        self.assertListEqual((custom_list1 - custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 2]))
        self.assertListEqual(custom_list2, CustomList([]))

        custom_list1 = CustomList([])
        custom_list2 = CustomList([3, 4])
        custom_list3 = CustomList([-3, -4])
        self.assertListEqual((custom_list1 - custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([]))
        self.assertListEqual(custom_list2, CustomList([3, 4]))

        custom_list1 = CustomList([1, 2, 3, 4])
        custom_list2 = CustomList([1, 9])
        custom_list3 = CustomList([0, -7, 3, 4])
        self.assertListEqual((custom_list1 - custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 2, 3, 4]))
        self.assertListEqual(custom_list2, CustomList([1, 9]))

        custom_list1 = CustomList([1, 9])
        custom_list2 = CustomList([1, 2, 3, 4])
        custom_list3 = CustomList([0, 7, -3, -4])
        self.assertListEqual((custom_list1 - custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 9]))
        self.assertListEqual(custom_list2, CustomList([1, 2, 3, 4]))

        custom_list1 = CustomList([1, 9, 3, 10])
        custom_list2 = CustomList([1, -2, 3, -4])
        custom_list3 = CustomList([0, 11, 0, 14])
        self.assertListEqual((custom_list1 - custom_list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([1, 9, 3, 10]))
        self.assertListEqual(custom_list2, CustomList([1, -2, 3, -4]))

        custom_list1 = CustomList([1, 9, 3, 10])
        custom_list2 = CustomList([5, -2, 1, -4])
        custom_list1 -= custom_list2
        custom_list3 = CustomList([-4, 11, 2, 14])
        self.assertListEqual(custom_list1, custom_list3)
        self.assertListEqual(custom_list2, CustomList([5, -2, 1, -4]))

        custom_list1 = CustomList([2.1, 9, 5.5, 10])
        list2 = [1, -2, 3, -4]
        custom_list3 = CustomList([1.1, 11, 2.5, 14])
        self.assertListEqual((custom_list1 - list2), custom_list3)
        self.assertListEqual(custom_list1, CustomList([2.1, 9, 5.5, 10]))
        self.assertListEqual(list2, [1, -2, 3, -4])

        list1 = [1, 9, 3, 10]
        custom_list2 = CustomList([3, 2.8, 3.5, -4])
        custom_list3 = CustomList([-2, 6.2, -0.5, 14])
        self.assertListEqual((list1 - custom_list2), custom_list3)
        self.assertListEqual(list1, [1, 9, 3, 10])
        self.assertListEqual(custom_list2, CustomList([3, 2.8, 3.5, -4]))

    def test_comparison(self):
        custom_list1 = CustomList([])
        custom_list2 = CustomList([])
        self.assertTrue(custom_list1 == custom_list2)
        self.assertFalse(custom_list1 != custom_list2)
        self.assertFalse(custom_list1 < custom_list2)
        self.assertTrue(custom_list1 <= custom_list2)
        self.assertFalse(custom_list1 > custom_list2)
        self.assertTrue(custom_list1 >= custom_list2)

        custom_list1 = CustomList([1])
        custom_list2 = CustomList([])
        self.assertFalse(custom_list1 == custom_list2)
        self.assertTrue(custom_list1 != custom_list2)
        self.assertFalse(custom_list1 < custom_list2)
        self.assertFalse(custom_list1 <= custom_list2)
        self.assertTrue(custom_list1 > custom_list2)
        self.assertTrue(custom_list1 >= custom_list2)

        custom_list1 = CustomList([1])
        custom_list2 = CustomList([10.2])
        self.assertFalse(custom_list1 == custom_list2)
        self.assertTrue(custom_list1 != custom_list2)
        self.assertTrue(custom_list1 < custom_list2)
        self.assertTrue(custom_list1 <= custom_list2)
        self.assertFalse(custom_list1 > custom_list2)
        self.assertFalse(custom_list1 >= custom_list2)

        custom_list1 = CustomList([5, 1, 3, 7])
        custom_list2 = CustomList([1, 8, 7])
        self.assertTrue(custom_list1 == custom_list2)
        self.assertFalse(custom_list1 != custom_list2)
        self.assertFalse(custom_list1 < custom_list2)
        self.assertTrue(custom_list1 <= custom_list2)
        self.assertFalse(custom_list1 > custom_list2)
        self.assertTrue(custom_list1 >= custom_list2)

    def test_str(self):
        builtin_list = []
        custom_list = CustomList(builtin_list)

        self.assertEqual(
            f"{sum(builtin_list)}:\t{str(builtin_list)}", str(custom_list)
        )

        builtin_list = [1]
        custom_list = CustomList(builtin_list)

        self.assertEqual(
            f"{sum(builtin_list)}:\t{str(builtin_list)}", str(custom_list)
        )

        builtin_list = [1, -3, 1.2, 123]
        custom_list = CustomList(builtin_list)

        self.assertEqual(
            f"{sum(builtin_list)}:\t{str(builtin_list)}", str(custom_list)
        )


if __name__ == "__main__":
    unittest.main()
