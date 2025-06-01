from manual_othello_agent import ManualOthelloAgent
from othello_interface import draw_board
from random_othello_agent import RandomOthelloAgent
from UCT_othello_agent import UCTOtelloAgent
from UCT_othello_agent_timed import UCTOtelloAgentTimed

from othello import OthelloGame

game = OthelloGame()

current_player = 2

player1 = UCTOtelloAgent(1)
player2 = UCTOtelloAgent(2)

while not game.has_finished():
  draw_board(game.board)
  #input()
  if game.get_valid_moves(current_player) != []:
      active_player = player1 if current_player==1 else player2
      move = active_player.choose_move(game)
      print(f"Player {current_player} played {move}")
      game = game.play_move(move, current_player)

  if current_player ==1:
     current_player = 2
  else:
     current_player = 1

white_points, black_points = game.get_results()
print(f"White points:{white_points}")
print(f"Black points:{black_points}")
if(white_points==black_points):
   print("It's a draw")
print(f"Winner is {"white" if white_points> black_points and black_points != white_points  else "black"}")
