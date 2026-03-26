import random

class HorizontalPreferenceAgent:
    def act(self, observation):
        board = observation["observation"]
        mask = observation["action_mask"]

        my_board = board[:, :, 0]
        legal_moves = [i for i, m in enumerate(mask) if m == 1]

        best_score = -1
        best_moves = []

        for col in legal_moves:
            row = self.get_next_open_row(my_board, col)

            if row is None:
                continue

            temp_board = my_board.copy()
            temp_board[row][col] = 1

            score = self.horizontal_score(temp_board, row, col)

            print(f"Kolom {col} -> score {score}")

            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)

        action = random.choice(best_moves)
        print("HORIZONTAL kiest:", action)
        return action

    def get_next_open_row(self, board, col):
        for row in reversed(range(6)):
            if board[row][col] == 0:
                return row
        return None

    def horizontal_score(self, board, row, col):
        score = 0

        # links tellen
        c = col - 1
        while c >= 0 and board[row][c] == 1:
            score += 1
            c -= 1

        # rechts tellen
        c = col + 1
        while c < 7 and board[row][c] == 1:
            score += 1
            c += 1

        return score