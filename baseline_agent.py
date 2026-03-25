import numpy as np
import random


class baseline:
    """
    Baseline agent voor Connect Four (PettingZoo compatible)

    Waarom baseline:
    - Simpele regels:
        1. Win indien mogelijk
        2. Blokkeer tegenstander
        3. Anders random zet

    Dit maakt het een referentie-agent voor vergelijking.
    """

    def act(self, observation):

        board = observation["observation"]
        mask = observation["action_mask"]

        legal_moves = [i for i, m in enumerate(mask) if m == 1]

        my_board = board[:, :, 0]
        opponent_board = board[:, :, 1]

        # 1. probeer zelf te winnen
        for col in legal_moves:

            row = self.get_next_open_row(my_board, col)
            if row is None:
                continue

            temp = my_board.copy()
            temp[row][col] = 1

            if self.check_win(temp):
                return col

        # 2. blokkeer tegenstander
        for col in legal_moves:

            row = self.get_next_open_row(opponent_board, col)
            if row is None:
                continue

            temp = opponent_board.copy()
            temp[row][col] = 1

            if self.check_win(temp):
                return col

        # 3. random zet
        return random.choice(legal_moves)

    def get_next_open_row(self, board, col):

        for row in reversed(range(6)):
            if board[row][col] == 0:
                return row

        return None

    def check_win(self, board):

        # horizontaal
        for r in range(6):
            for c in range(4):
                if all(board[r][c+i] == 1 for i in range(4)):
                    return True

        # verticaal
        for r in range(3):
            for c in range(7):
                if all(board[r+i][c] == 1 for i in range(4)):
                    return True

        # diagonaal \
        for r in range(3):
            for c in range(4):
                if all(board[r+i][c+i] == 1 for i in range(4)):
                    return True

        # diagonaal /
        for r in range(3, 6):
            for c in range(4):
                if all(board[r-i][c+i] == 1 for i in range(4)):
                    return True

        return False