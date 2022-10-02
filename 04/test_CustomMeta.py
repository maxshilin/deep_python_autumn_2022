import unittest

from CustomMeta import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_no_setattr(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

            @classmethod
            def classmethod(cls, arg):
                return str(arg)

        # pylint: disable=no-member,pointless-statement

        self.assertEqual(CustomClass.custom_x, 50)

        with self.assertRaises(AttributeError) as manager:
            CustomClass.x

        self.assertEqual(
            str(manager.exception),
            "type object 'CustomClass' has no attribute 'x'",
        )

        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)

        with self.assertRaises(AttributeError) as manager:
            inst.x

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'x'",
        )

        self.assertEqual(inst.custom_val, 99)

        with self.assertRaises(AttributeError) as manager:
            inst.val

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'val'",
        )

        self.assertEqual(inst.custom_line(), 100)

        with self.assertRaises(AttributeError) as manager:
            inst.line()

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'line'",
        )

        self.assertEqual(inst.custom_classmethod("hello world"), "hello world")

        with self.assertRaises(AttributeError) as manager:
            inst.classmethod("hello world")

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'classmethod'",
        )

        self.assertEqual(str(inst), "Custom_by_metaclass")

        # pylint: disable=attribute-defined-outside-init
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")

        with self.assertRaises(AttributeError) as manager:
            inst.dynamic

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'dynamic'",
        )

        with self.assertRaises(AttributeError) as manager:
            inst.yyy

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'yyy'",
        )

    def test_setattr(self):
        # pylint: disable=too-few-public-methods
        class CustomClass(metaclass=CustomMeta):
            def __init__(self, val):
                self.val = val

            def __setattr__(self, name, value):
                super().__setattr__(name, value)
                super().__setattr__(f"modified_{name}", value * 2)

        inst = CustomClass(10)
        # pylint: disable=no-member,pointless-statement

        self.assertEqual(inst.custom_val, 10)
        self.assertEqual(inst.custom_modified_val, 20)

        with self.assertRaises(AttributeError) as manager:
            inst.val

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'val'",
        )

        with self.assertRaises(AttributeError) as manager:
            inst.modified_val

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'modified_val'",
        )

        inst.dynamic = 50  # pylint: disable=attribute-defined-outside-init

        self.assertEqual(inst.custom_dynamic, 50)
        self.assertEqual(inst.custom_modified_dynamic, 100)

        with self.assertRaises(AttributeError) as manager:
            inst.dynamic

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'dynamic'",
        )

        with self.assertRaises(AttributeError) as manager:
            inst.modified_dynamic

        self.assertEqual(
            str(manager.exception),
            "'CustomClass' object has no attribute 'modified_dynamic'",
        )


if __name__ == "__main__":
    unittest.main()
