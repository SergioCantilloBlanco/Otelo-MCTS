from othello import Othello
from agents.random_othello_agent import RandomOthelloAgent
juego = Othello()

current_player = 2

player1 = RandomOthelloAgent()
player2 = RandomOthelloAgent()

while not juego.has_finished():
  if juego.get_valid_moves(current_player) != []:
      active_player = player1 if current_player==1 else player2
      juego.jugar_movimiento(active_player.choose_move(juego), current_player)

  current_player = (current_player+1)%2

print(juego.tablero)
