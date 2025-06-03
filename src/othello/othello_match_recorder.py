import copy

import numpy as np
from manual_othello_agent import ManualOthelloAgent
from othello_interface import draw_board
from random_othello_agent import RandomOthelloAgent
from tqdm import tqdm
from UCT_othello_agent import UCTOtelloAgent

from othello import OthelloGame

n = 100

for i in tqdm(range(n)):
  game = OthelloGame()

  current_player = 2
  game_states = [(game.board, current_player)]
  player1 = UCTOtelloAgent(1)
  player2 = UCTOtelloAgent(2)

  while not game.has_finished():
    # draw_board(game.board)
    if game.get_valid_moves(current_player) != []:
        active_player = player1 if current_player==1 else player2
        move = active_player.choose_move(game)
        game = game.play_move(move, current_player)
        game_states.append((copy.deepcopy(game.board), current_player))

    if current_player == 1:
      current_player = 2
    else:
      current_player = 1

  white_points, black_points = game.get_results()
  for board, player in game_states:
    if white_points == black_points:
        label = 0
    else:
        winner = 1 if white_points > black_points else -1
        label = winner if player == 1 else -winner
    labeled_states.append((board, label))

np.save("labeled_game_states.npy", np.array(labeled_states, dtype=object))
