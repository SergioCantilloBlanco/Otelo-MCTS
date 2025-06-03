import copy

import numpy as np
from manual_othello_agent import ManualOthelloAgent
from othello_interface import draw_board
from random_othello_agent import RandomOthelloAgent
from tqdm import tqdm
from UCT_othello_agent import UCTOtelloAgent

from othello import OthelloGame

n = 15

labeled_states = []

agent1wins = 0
agent2wins = 0
draws = 0
agent1points = 0
agent2points = 0

for i in tqdm(range(n)):
  game = OthelloGame()

  current_player = 2
  player2 = UCTOtelloAgent(2, 30)
  player1 = RandomOthelloAgent(1)

  while not game.has_finished():
    draw_board(game.board)
    if game.get_valid_moves(current_player) != []:
        active_player = player1 if current_player==1 else player2
        move = active_player.choose_move(game)
        game = game.play_move(move, current_player)

    if current_player == 1:
      current_player = 2
    else:
      current_player = 1

  white_points, black_points = game.get_results()
  if white_points == black_points:
    draws += 1
  elif white_points > black_points: 
    agent1wins += 1
  else:
    agent2wins  += 1

  agent1points += white_points
  agent2points += black_points

print(agent1wins/n*100)
print(agent2wins/n*100)

