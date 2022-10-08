import unittest
import unittest.mock
from io import StringIO

from filter_file import FilterFile


class TestLRUCache(unittest.TestCase):
    @unittest.mock.patch("builtins.open")
    def test_empty_fields(self, open_mock):
        file = StringIO("")
        open_mock.return_value = file
        output = []

        gen = FilterFile(file, [])
        self.assertEqual(list(gen), output)

        file = StringIO("Hello world!\nHi universe!\nHello Sun!")
        open_mock.return_value = file
        output = []

        gen = FilterFile(file, [])
        self.assertEqual(list(gen), output)

        file = StringIO("")
        open_mock.return_value = file
        output = []

        gen = FilterFile(file, ["hello"])
        self.assertEqual(list(gen), output)

    @unittest.mock.patch("builtins.open")
    def test_generator(self, open_mock):
        file = StringIO("Hello world!\nHi universe!\nHeLlo Sun!")
        open_mock.return_value = file
        output = ["Hello world!\n", "HeLlo Sun!"]

        gen = FilterFile(file, ["hello"])
        self.assertEqual(list(gen), output)

        file = StringIO(
            "Ну Сталкер обалдел\nА в кустах, значит, сталкер сидит и"
            " тихо прячется\nОдин сталкер другому говорит\nВ общем"
            " Сталкер пришел к доктору и говорит\nКомандир с просьбой"
            " в голосе отпусти ты меня\nВот говорили мне что пить вредно"
            " а я не слушался грустным голосом\nА ведь верно думает вслух"
            " да Ежели я бы трезвый был разве сунулся сюда вчера с"
            " издевкой ж вся Зона видела\n"
        )

        open_mock.return_value = file
        gen = FilterFile(file, ["сталкер", "зона"])
        output = [
            "Ну Сталкер обалдел\n",
            "А в кустах, значит, сталкер сидит и тихо прячется\n",
            "Один сталкер другому говорит\n",
            "В общем Сталкер пришел к доктору и говорит\n",
            (
                "А ведь верно думает вслух"
                " да Ежели я бы трезвый был разве сунулся сюда вчера с"
                " издевкой ж вся Зона видела\n"
            ),
        ]

        self.assertEqual(list(gen), output)

    @unittest.mock.patch("builtins.open")
    def test_raise_stop_iteration(self, open_mock):
        file = StringIO("Hello world!\nHi universe!\nHeLlo Sun!")
        open_mock.return_value = file
        output = ["Hello world!\n", "HeLlo Sun!"]

        gen = FilterFile(file, ["hello"])
        self.assertEqual(list(gen), output)

        with self.assertRaises(StopIteration):
            next(gen)


if __name__ == "__main__":
    unittest.main()
