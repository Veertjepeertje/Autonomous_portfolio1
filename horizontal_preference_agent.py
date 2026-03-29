import random
import numpy as np


class HorizontalPreferenceAgent:
    """
    Rule-based agent voor PettingZoo Connect Four.
    Kiest de legale zet die de beste horizontale aansluiting met eigen stenen oplevert.

    Bordrepresentatie:
    - observation["observation"] heeft shape (6, 7, 2)
    - kanaal 0 = huidige speler
    - kanaal 1 = tegenstander
    """

    def act(self, observation):
        board = observation["observation"]
        action_mask = observation["action_mask"]

        # Eigen bordlaag
        my_board = board[:, :, 0]

        # Legale kolommen
        legal_moves = [col for col, allowed in enumerate(action_mask) if allowed == 1]

        if not legal_moves:
            return None

        best_score = -1
        best_moves = []

        for col in legal_moves:
            row = self.get_next_open_row(my_board, col)

            if row is None:
                continue

            # Simuleer zet
            temp_board = my_board.copy()
            temp_board[row][col] = 1

            # Bereken horizontale score
            score = self.horizontal_score(temp_board, row, col)

            print(f"Kolom {col} -> horizontale score {score}")

            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)

        if not best_moves:
            return random.choice(legal_moves)

        action = random.choice(best_moves)
        print("HORIZONTAL kiest:", action)
        return action

    def get_next_open_row(self, board, col):
        """
        Geeft de onderste vrije rij in een kolom terug.
        """
        for row in reversed(range(6)):
            if board[row][col] == 0:
                return row
        return None

    def horizontal_score(self, board, row, col):
        """
        Berekent de lengte van de horizontale rij die ontstaat
        na het plaatsen van een steen op (row, col).
        De nieuw geplaatste steen telt mee.
        """
        score = 1  # de geplaatste steen zelf

        # Kijk naar links
        c = col - 1
        while c >= 0 and board[row][c] == 1:
            score += 1
            c -= 1

        # Kijk naar rechts
        c = col + 1
        while c < 7 and board[row][c] == 1:
            score += 1
            c += 1

        return score
        