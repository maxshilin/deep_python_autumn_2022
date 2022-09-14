import unittest
import unittest.mock
from game import TicTac


class TestEvens(unittest.TestCase):
    def test_check_correct_input(self):
        game = TicTac()

        for i in range(1, 10):
            self.assertEqual(game.validate_input(f" {i} "), i)

        self.assertEqual(game.validate_input("\u0661"), 1)

    @unittest.mock.patch("builtins.print")
    def test_check_incorrect_int_input(self, input_mock):
        input_mock.return_value = None
        game = TicTac()

        for i in range(10, 21):
            self.assertIsNone(game.validate_input(f"{i}"))

        for i in range(-10, 1):
            self.assertIsNone(game.validate_input(f"{i}"))

    @unittest.mock.patch("builtins.print")
    def test_check_incorrect_input(self, input_mock):
        input_mock.return_value = None
        game = TicTac()

        self.assertIsNone(game.validate_input(""))
        self.assertIsNone(game.validate_input(" "))
        self.assertIsNone(game.validate_input("a"))
        self.assertIsNone(game.validate_input("asdfdsdg"))
        self.assertIsNone(game.validate_input("1.2"))
        self.assertIsNone(game.validate_input("5.31"))
        self.assertIsNone(game.validate_input("-1.37"))
        self.assertIsNone(game.validate_input("-12.45"))
        self.assertIsNone(game.validate_input("²"))
        self.assertIsNone(game.validate_input("² ⅘"))
        self.assertIsNone(game.validate_input("⅓"))
        self.assertIsNone(game.validate_input("\u0660"))

    @unittest.mock.patch("builtins.print")
    def test_check_occupied_cell(self, input_mock):
        input_mock.return_value = None
        board = ["X" for _ in range(9)]
        game = TicTac(board)

        for i in range(1, 10):
            self.assertIsNone(game.validate_input(f"{i}"))

        board = ["O" for _ in range(9)]
        game = TicTac(board)

        for i in range(1, 10):
            self.assertIsNone(game.validate_input(f"{i}"))

    def test_check_winner(self):
        board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", " ", "X", "X", "X", " ", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", " ", " ", " ", " ", "X", "X", "X"]
        self.assertTrue(TicTac(board).check_winner())

        board = ["X", " ", " ", "X", " ", " ", "X", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", "X", " ", " ", "X", " ", " ", "X", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", "X", " ", " ", "X", " ", " ", "X"]
        self.assertTrue(TicTac(board).check_winner())

        board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", "X", " ", "X", " ", "X", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = ["O", "O", "O", " ", " ", " ", " ", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", " ", "O", "O", "O", " ", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", " ", " ", " ", " ", "O", "O", "O"]
        self.assertTrue(TicTac(board).check_winner())

        board = ["O", " ", " ", "O", " ", " ", "O", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", "O", " ", " ", "O", " ", " ", "O", " "]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", "O", " ", " ", "O", " ", " ", "O"]
        self.assertTrue(TicTac(board).check_winner())

        board = ["O", " ", " ", " ", "O", " ", " ", " ", "O"]
        self.assertTrue(TicTac(board).check_winner())

        board = [" ", " ", "O", " ", "O", " ", "O", " ", " "]
        self.assertTrue(TicTac(board).check_winner())

    def test_check_not_winner(self):
        for i in range(9):
            board = [" " for _ in range(9)]
            board[i] = "X"
            self.assertFalse(TicTac(board).check_winner())

        for i in range(9):
            board = [" " for _ in range(9)]
            board[i] = "O"
            self.assertFalse(TicTac(board).check_winner())

        board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.assertFalse(TicTac(board).check_winner())

        board = ["X", "O", "X", " ", " ", " ", " ", " ", " "]
        self.assertFalse(TicTac(board).check_winner())

        board = [" ", " ", " ", "O", "X", "X", " ", " ", " "]
        self.assertFalse(TicTac(board).check_winner())

        board = [" ", " ", " ", " ", " ", " ", "X", "X", "O"]
        self.assertFalse(TicTac(board).check_winner())

        board = ["X", " ", " ", "X", " ", " ", "O", " ", " "]
        self.assertFalse(TicTac(board).check_winner())

        board = [" ", "X", " ", " ", "O", " ", " ", "X", " "]
        self.assertFalse(TicTac(board).check_winner())

        board = [" ", " ", "O", " ", " ", "X", " ", " ", "X"]
        self.assertFalse(TicTac(board).check_winner())

        board = ["O", " ", " ", " ", "X", " ", " ", " ", "X"]
        self.assertFalse(TicTac(board).check_winner())

        board = [" ", " ", "X", " ", "O", " ", "X", " ", " "]
        self.assertFalse(TicTac(board).check_winner())

        board = ["X", "O", "X", "O", "O", "X", "X", "X", "O"]
        self.assertFalse(TicTac(board).check_winner())

    @unittest.mock.patch("builtins.print")
    @unittest.mock.patch("builtins.input")
    def test_check_start_game(self, input_mock, print_mock):
        print_mock.return_value = None

        game = TicTac()
        input_mock.side_effect = ["1", "2", "3", "4", "6", "5", "7", "9", "8"]
        self.assertEqual(game.start_game(), None)

        game = TicTac()
        input_mock.side_effect = ["1", "2", "3", "4", "5", "6", "7"]
        self.assertEqual(game.start_game(), "X")

        game = TicTac()
        input_mock.side_effect = ["1", "2", "4", "3", "7"]
        self.assertEqual(game.start_game(), "X")

        game = TicTac()
        input_mock.side_effect = ["1", "4", "3", "5", "2"]
        self.assertEqual(game.start_game(), "X")

        game = TicTac()
        input_mock.side_effect = ["2", "1", "3", "5", "4", "9"]
        self.assertEqual(game.start_game(), "O")

        game = TicTac()
        input_mock.side_effect = ["1", "2", "3", "5", "4", "8"]
        self.assertEqual(game.start_game(), "O")

        game = TicTac()
        input_mock.side_effect = ["4", "1", "9", "2", "5", "3"]
        self.assertEqual(game.start_game(), "O")
