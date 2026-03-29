import numpy as np
import random

class BlockingAgent:
    """
    Strategie:
    1. Blokkeer directe win tegenstander
    2. Win als mogelijk
    3. Blokkeer fork (dubbele dreiging)
    4. Blokkeer echte 3-op-een-rij dreiging (die tot winst kan leiden)
    5. Kies een veilige zet (die niet leidt tot directe winst voor de tegenstander)
    5. Random zet
    """

    def act(self, observation):

        board = observation["observation"]
        mask = observation["action_mask"]

        legal_moves = [i for i, m in enumerate(mask) if m == 1]
        my_board = board[:, :, 0]
        opponent_board = board[:, :, 1]

        # 🔴 0. MUST BLOCK (ABSOLUTE PRIORITEIT)
        must_block = []

        for col in legal_moves:
            row = self.get_next_open_row(opponent_board, col)
            if row is None:
                continue

            temp = opponent_board.copy()
            temp[row][col] = 1

            if self.check_win(temp):
                must_block.append(col)

        if must_block:
            print("MUST BLOCK:", must_block)
            return random.choice(must_block)

        #1. WIN ALS MOGELIJK
        for col in legal_moves:
            row = self.get_next_open_row(my_board, col)
            if row is None:
                continue

            temp = my_board.copy()
            temp[row][col] = 1

            if self.check_win(temp):
                print("WIN:", col)
                return col

        #2. DIRECTE WIN BLOKKEREN
        for col in legal_moves:
            row = self.get_next_open_row(opponent_board, col)
            if row is None:
                continue

            temp = opponent_board.copy()
            temp[row][col] = 1

            if self.check_win(temp):
                print("BLOCK WIN:", col)
                return col
            
        #filter veilige zetten 
        safe_moves = []

        for col in legal_moves:
            row = self.get_next_open_row(my_board, col)
            if row is None:
                continue

            temp_my = my_board.copy()
            temp_my[row][col] = 1

            # Simuleer tegenstander daarna
            opponent_can_win = False

            for opp_col in range(7):
                opp_row = self.get_next_open_row(opponent_board, opp_col)
                if opp_row is None:
                    continue

                temp_opp = opponent_board.copy()
                temp_opp[opp_row][opp_col] = 1

                if self.check_win(temp_opp):
                    opponent_can_win = True
                    break

            if not opponent_can_win:
                safe_moves.append(col)

        if safe_moves:
            legal_moves = safe_moves


        #3. FORK BLOKKEREN
        for col in legal_moves:
            row = self.get_next_open_row(opponent_board, col)
            if row is None:
                continue

            temp = opponent_board.copy()
            temp[row][col] = 1

            future_wins = self.count_winning_moves(temp)

            if future_wins >= 2:
                print("BLOCK FORK:", col)
                return col

        #4. ECHTE 3-OP-EEN-RIJ DREIGING BLOKKEREN
        threat_moves = []

        for col in legal_moves:
            row = self.get_next_open_row(opponent_board, col)
            if row is None:
                continue

            if self.is_real_threat(opponent_board, row, col):
                threat_moves.append(col)

        if threat_moves:
            print("BLOCK THREAT:", threat_moves)
            return random.choice(threat_moves)

        #5. RANDOM
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

    def is_real_threat(self, board, row, col):

        temp = board.copy()
        temp[row][col] = 1

        # check alle richtingen op EXACT 3 + 1 lege plek
        return (
            self.check_line(temp, row, col, 0, 1) or  # horizontaal
            self.check_line(temp, row, col, 1, 0) or  # verticaal
            self.check_line(temp, row, col, 1, 1) or  # diag \
            self.check_line(temp, row, col, 1, -1)    # diag /
        )

    def check_line(self, board, row, col, dr, dc):

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

        return count == 3