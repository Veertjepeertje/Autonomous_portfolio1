import random

class MiddleFirstAgent:
    """
    Strategy:
    1. Kies middenkolom (3)
    2. Kies kolommen naast midden (2, 4)
    3. Anders random
    """

    def act(self, observation):
        mask = observation["action_mask"]
        legal_moves = [i for i, m in enumerate(mask) if m == 1]

        # Regel 1: midden
        if 3 in legal_moves:
            return 3

        # Regel 2: naast midden (meer strategisch dan random)
        for move in [2, 4]:
            if move in legal_moves:
                return move

        # Regel 3: random fallback
        return random.choice(legal_moves)
