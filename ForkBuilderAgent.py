import random
import numpy as np


class ForkBuilderAgent:
    """
    Agent voor Connect Four die de volgende prioriteiten gebruikt:
    1. Direct winnen
    2. Directe winst van de tegenstander blokkeren
    3. Een fork creëren
    4. Een fork van de tegenstander blokkeren
    5. De middelste kolom spelen
    6. Terugvallen op een willekeurige geldige zet
    """

    def __init__(self, env=None,player_id=0):
        self.env =env
        self.player_id=player_id

    def get_next_open_row(self, board,col):
        for r in range(board.shape[0] - 1, -1, -1):
            if board[r][col] == 0:
                return r
        return None

    def check_win(self,board):
        rows, cols =board.shape

        # Horizontaal
        for r in range(rows):
            for c in range(cols - 3):
                if all(board[r][c + i] == 1 for i in range(4)):
                    return True

        # Verticaal
        for r in range(rows - 3):
            for c in range(cols):
                if all(board[r + i][c] == 1 for i in range(4)):
                    return True

        # Diagonaal omlaag-rechts
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(board[r + i][c + i] == 1 for i in range(4)):
                    return True

        # Diagonaal omhoog-rechts
        for r in range(3, rows):
            for c in range(cols - 3):
                if all(board[r - i][c + i] == 1 for i in range(4)):
                    return True

        return False

    def get_valid_moves(self, action_mask):
        return [c for c in range(len(action_mask)) if action_mask[c] == 1]

    def get_immediate_winning_moves(self, board, valid_moves):
        winning_moves = []

        for col in valid_moves:
            row = self.get_next_open_row(board, col)
            if row is not None:
                temp_board = board.copy()
                temp_board[row][col] = 1

                if self.check_win(temp_board):
                    winning_moves.append(col)

        return winning_moves

    def count_future_winning_moves(self, board, action_mask):
        valid_moves = self.get_valid_moves(action_mask)
        return len(self.get_immediate_winning_moves(board, valid_moves))

    def creates_fork(self, board, action_mask, col):
        row = self.get_next_open_row(board, col)
        if row is None:
            return False

        temp_board = board.copy()
        temp_board[row][col] = 1

        future_wins = self.count_future_winning_moves(temp_board, action_mask)
        return future_wins >= 2

    def get_fork_moves(self, board, action_mask):
        valid_moves=self.get_valid_moves(action_mask)
        fork_moves = []

        for col in valid_moves:
            if self.creates_fork(board, action_mask, col):
                fork_moves.append(col)

        return fork_moves

    def simulate_opponent_fork_after_move(self, my_board, opp_board, action_mask, my_move):
        """
        Simuleer eerst onze zet. Controleer daarna of de tegenstander
        een fork kan creëren.
        Geeft een lijst terug met fork-zetten van de tegenstander
        na onze zet.
        """
        row = self.get_next_open_row(my_board, my_move)
        if row is None:
            return []

        temp_my_board = my_board.copy()
        temp_opp_board = opp_board.copy()
        temp_my_board[row][my_move] = 1

        valid_moves_after= self.get_valid_moves(action_mask)
        opponent_fork_moves = []

        for opp_col in valid_moves_after:
            opp_row = self.get_next_open_row(temp_opp_board, opp_col)
            if opp_row is None:
                continue

            opp_future_board = temp_opp_board.copy()
            opp_future_board[opp_row][opp_col] = 1

            future_wins = self.get_immediate_winning_moves(
                opp_future_board,
                valid_moves_after
            )

            if len(future_wins) >= 2:
                opponent_fork_moves.append(opp_col)

        return opponent_fork_moves

    def select_action(self, observation, *args, **kwargs):
        board = np.array(observation["observation"]).reshape(6, 7, 2)
        action_mask = observation["action_mask"]

        my_board= board[:, :, 0]
        opp_board= board[:, :, 1]

        valid_moves = self.get_valid_moves(action_mask)

        if not valid_moves:
            return None

        # 1. Direct winnen
        for col in valid_moves:
            row = self.get_next_open_row(my_board, col)
            if row is not None:
                temp_board = my_board.copy()
                temp_board[row][col] = 1

                if self.check_win(temp_board):
                    return col

        # 2. Directe winst van de tegenstander blokkeren
        for col in valid_moves:
            row = self.get_next_open_row(opp_board, col)
            if row is not None:
                temp_board = opp_board.copy()
                temp_board[row][col]= 1

                if self.check_win(temp_board):
                    return col

        # 3. Een fork creëren
        my_forks = self.get_fork_moves(my_board, action_mask)
        if my_forks:
            center_preference =[3, 2, 4, 1, 5, 0, 6]
            for col in center_preference:
                if col in my_forks:
                    return col

        # 4. Een fork van de tegenstander blokkeren
        opp_forks = self.get_fork_moves(opp_board, action_mask)
        if opp_forks:
            # Speel indien mogelijk direct in een fork-kolom van de tegenstander
            for col in [3, 2, 4, 1,5, 0, 6]:
                if col in opp_forks and col in valid_moves:
                    return col

            
            best_move = None
            best_score = float("inf")

            for my_move in valid_moves:
                opponent_fork_count=len(
                    self.simulate_opponent_fork_after_move(
                        my_board, opp_board, action_mask, my_move
                    )
                )

                if opponent_fork_count < best_score:
                    best_score= opponent_fork_count
                    best_move=my_move

            if best_move is not None:
                return best_move

        # Geef voorkeur aan de middelste kolom
        if 3 in valid_moves:
            return 3

        #Geef voorkeur aan kolommen dicht bij het midden
        for col in [2,4, 1, 5, 0, 6]:
            if col in valid_moves:
                return col

        # Willekeurige fallback
        return random.choice(valid_moves)