from othello.othello_agent import OthelloAgent
from othello.othello import Othello
import random
class RandomOthelloAgent(OthelloAgent):
  def choose_move(self, game: Othello ):
    return random.choice(game.get_valid_moves)
