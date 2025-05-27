from othello import OthelloGame


class Node():
    def __init__(self, state:OthelloGame, player, previous_action=None ,parent=None):
        self.state = state
        self.parent = parent
        self.previous_action = previous_action
        self.player = player
        self.children = []
        self.unused_actions = state.get_valid_moves(player)
        self.accumulated_rewards = 0
        self.visits = 0

    def is_fully_expanded(self):
        return len(self.unused_actions) == 0
        

   