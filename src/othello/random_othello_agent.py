import random

from othello_agent import OthelloAgent

from othello import OthelloGame


class RandomOthelloAgent(OthelloAgent):
  def choose_move(self, game: OthelloGame ):
    return random.choice(game.get_valid_moves(self.player))
