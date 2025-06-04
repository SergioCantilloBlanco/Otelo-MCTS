import copy

import numpy as np
from manual_othello_agent import ManualOthelloAgent
from othello_interface import draw_board
from random_othello_agent import RandomOthelloAgent
from tqdm import tqdm
from UCT_othello_agent import UCTOtelloAgent

from othello import OthelloGame

# from neural_UCT_othello_agent import NeuralUCTOtelloAgent


n = 50


agent_1_wins = 0
agent_2_wins = 0
draws = 0

for i in tqdm(range(n)):
  game = OthelloGame()

  current_player = 2
  player2 = UCTOtelloAgent(2, 100)
  player1 = UCTOtelloAgent(1, 10)
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
  draw_board(game.board)
  if white_points == black_points:
    print("DRAW")
    draws += 1
  elif white_points > black_points:
    agent_1_wins += 1
    print("White Wins")
  else:
    agent_2_wins  += 1
    print("Black Wins")

print(f"Agent 1 wins {(agent_1_wins/n)*100}")
print(f"Agent 2 wins {(agent_2_wins/n)*100}")
print(f"Draws {(draws/n)*100}")
