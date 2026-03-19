import numpy as np
import random

class BlockingAgent:

    def act(self, observation):

        board = observation["observation"]
        mask = observation["action_mask"]

        legal_moves = [i for i, m in enumerate(mask) if m == 1]

        opponent = board[:, :, 1]

        # 🔥 check elke kolom: voorkomt directe winst
        for col in legal_moves:

            row = self.get_next_open_row(opponent, col)
            if row is None:
                continue

            temp_board = opponent.copy()
            temp_board[row][col] = 1

            if self.check_win(temp_board):
                print("BLOCKING WIN:", col)
                return col

        # 🔥 extra: detecteer 3-op-een-rij dreigingen
        for col in legal_moves:

            row = self.get_next_open_row(opponent, col)
            if row is None:
                continue

            if self.creates_threat(opponent, row, col):
                print("BLOCKING THREAT:", col)
                return col

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

    def creates_threat(self, board, row, col):

        temp = board.copy()
        temp[row][col] = 1

        # tel aantal 3-op-een-rij
        count = 0

        # horizontaal
        for c in range(max(0, col-3), min(4, col+1)):
            window = temp[row][c:c+4]
            if np.sum(window) == 3:
                count += 1

        # verticaal
        for r in range(max(0, row-3), min(3, row+1)):
            window = [temp[r+i][col] for i in range(4)]
            if sum(window) == 3:
                count += 1

        # diagonaal \
        for i in range(-3, 1):
            coords = [(row+i+j, col+i+j) for j in range(4)]
            if all(0 <= r < 6 and 0 <= c < 7 for r, c in coords):
                window = [temp[r][c] for r, c in coords]
                if sum(window) == 3:
                    count += 1

        # diagonaal /
        for i in range(-3, 1):
            coords = [(row-i-j, col+i+j) for j in range(4)]
            if all(0 <= r < 6 and 0 <= c < 7 for r, c in coords):
                window = [temp[r][c] for r, c in coords]
                if sum(window) == 3:
                    count += 1

        return count > 0