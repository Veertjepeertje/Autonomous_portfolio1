import numpy as np
import random

class BlockingAgent:

    def act(self, observation):

        board = observation["observation"]
        mask = observation["action_mask"]

        legal_moves = [i for i, m in enumerate(mask) if m == 1]

        opponent = board[:, :, 1]

        # 🔴 1. DIRECTE WIN BLOCKEN
        for col in legal_moves:
            row = self.get_next_open_row(opponent, col)
            if row is None:
                continue

            temp = opponent.copy()
            temp[row][col] = 1

            if self.check_win(temp):
                print("BLOCK WIN:", col)
                return col

        # 🟡 2. 3-OP-EEN-RIJ DREIGING BLOCKEN
        threat_moves = []

        for col in legal_moves:
            row = self.get_next_open_row(opponent, col)
            if row is None:
                continue

            if self.is_threat(opponent, row, col):
                threat_moves.append(col)

        if threat_moves:
            print("BLOCK THREAT:", threat_moves)
            return random.choice(threat_moves)
        
        # 🟠 FORK BLOCKEN
        for col in legal_moves:

            row = self.get_next_open_row(opponent, col)
            if row is None:
                continue

            temp = opponent.copy()
            temp[row][col] = 1

            future_wins = self.count_winning_moves(temp)

            if future_wins >= 2:
                print("BLOCK FORK:", col)
                return col

        # 🔵 3. RANDOM
        return random.choice(legal_moves)

    def get_next_open_row(self, board, col):
        for row in reversed(range(6)):
            if board[row][col] == 0:
                return row
        return None
    
    def count_winning_moves(self, board):

        winning_moves = 0

        for col in range(7):
            row = self.get_next_open_row(board, col)
            if row is None:
                continue

            temp = board.copy()
            temp[row][col] = 1

            if self.check_win(temp):
                winning_moves += 1

        return winning_moves

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

    def is_threat(self, board, row, col):

        temp = board.copy()
        temp[row][col] = 1

        # check alle richtingen op 3-op-een-rij
        return self.count_in_row(temp, row, col) >= 3

    def count_in_row(self, board, row, col):

        def count_dir(dr, dc):
            count = 1

            # forward
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == 1:
                count += 1
                r += dr
                c += dc

            # backward
            r, c = row - dr, col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == 1:
                count += 1
                r -= dr
                c -= dc

            return count

        # check alle richtingen
        directions = [(0,1), (1,0), (1,1), (1,-1)]

        return max(count_dir(dr, dc) for dr, dc in directions)