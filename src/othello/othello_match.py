from othello import OthelloGame
from random_othello_agent import RandomOthelloAgent
from othello_interface import draw_board

game = OthelloGame()

current_player = 2

player1 = RandomOthelloAgent(1)
player2 = RandomOthelloAgent(2)

while not game.has_finished():
  draw_board(game.board)
  input()
  if game.get_valid_moves(current_player) != []:
      active_player = player1 if current_player==1 else player2
      game.play_move(active_player.choose_move(game), current_player)

  if current_player ==1:
     current_player = 2
  else:
     current_player = 1
