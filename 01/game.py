class TicTac:
    def __init__(self, board=None):
        if board is None:
            self.board = [" " for _ in range(9)]
        else:
            self.board = board

    def show_board(self):
        dashes = "_" * 5
        spaces = " " * 5
        board = self.board
        print(f'{"_"*19}')

        for i in range(3):
            print(f"|{spaces}|{spaces}|{spaces}|")
            print(f"|  {board[3*i]}  |  {board[3*i+1]}  |  {board[3*i+2]}  |")
            print(f"|{dashes}|{dashes}|{dashes}|")

        print("\n")

    def validate_input(self, num):
        num = num.replace(" ", "")

        if num.isdecimal() and num.isnumeric():
            if int(num) <= 9 and int(num) >= 1:
                if self.board[int(num) - 1] == " ":
                    return int(num)

                print("Error. This cell is already occupied")
            else:
                print("Error. Your number should be 1-9")

        elif (
            num.replace("-", "").isnumeric()
            and not num.replace("-", "").isdecimal()
        ):
            print("Error. Don't use ASCII characters")

        elif num.replace("-", "").isnumeric():
            print("Error. Your number should be 1-9")

        else:
            print("Error. Your should enter an integer number")
        return None

    def start_game(self):
        self.show_board()

        for i in range(9):
            num = None
            player = "X" if i % 2 == 0 else "O"
            while num is None:
                num = self.validate_input(
                    input(f'Player "{player}" enter integer number 1-9: ')
                )

            self.board[num - 1] = player
            self.show_board()

            if self.check_winner():
                print(f'Player "{player}" won the game!')
                return player

        print("It's draw!")
        return None

    def check_winner(self):
        board = self.board
        for i in range(3):
            if board[3 * i] == board[3 * i + 1] == board[3 * i + 2] != " ":
                return True

            if board[i] == board[i + 3] == board[i + 6] != " ":
                return True

        if board[0] == board[4] == board[8] != " ":
            return True

        if board[2] == board[4] == board[6] != " ":
            return True

        return False


if __name__ == "__main__":
    game = TicTac()
    game.start_game()
