import numpy as np

directions = [(1,0), (-1,0), (0,1), (0,-1) , (1,1) , (1,-1), (-1,1) ,(-1,-1)]

def create_new_board():
    board = np.zeros((8,8),dtype=int)

    board[3,3] = 1
    board[4,4] = 1
    board[4,3] = 2
    board[3,4] = 2
    return board

def update_line(board, position, player, direction):
    keep_searching = True
    row,column = position
    row_direction, column_direction = direction
    positions_to_invert = []
    while(keep_searching):
        row += row_direction
        column += column_direction

        if not (0 <= row <= 7 and 0 <= column <= 7):
          keep_searching = False
          break


        if(board[row,column] == 0):
            keep_searching = False
        elif(board[row,column] != player):
            positions_to_invert.append((row, column))
        else:
            for position_to_invert in positions_to_invert:
                row_to_invert,column_to_invert = position_to_invert
                board[row_to_invert,column_to_invert]  = player
            keep_searching = False
    return board

def get_valid_moves(board, player):

    valid_moves = []

    for row in range(8):
        for column in range(8):
            if board[row,column] == 0:
              if(check_valid_move(board, (row,column), player)):
                  valid_moves.append((row, column))
    return valid_moves


def check_valid_move_in_direction(board, position, player, direction):
    keep_searching = True
    row,column = position
    row_direction, column_direction = direction
    found_an_oposite_tile_between = False
    while(keep_searching):
        row += row_direction
        column += column_direction


        if not (0 <= row <= 7 and 0 <= column <= 7):
          return False

        if(board[row,column] == 0):
            return False
        elif(board[row,column] != player):
            found_an_oposite_tile_between = True
        else:
            return found_an_oposite_tile_between
def update_board(board, position, player):
      fila,columna = position
      board[fila,columna] = player

      for direccion in directions:
        board = update_line(board.copy(), position, player, direccion)


      return board

def check_valid_move(board, position, player):
    row, column = position
    for direction in directions:
      if check_valid_move_in_direction(board, (row, column) , player, direction):
        return True
    return False

def has_finished(board):
   return not np.any(board == 0)

def get_results(board):
  white_points = np.count_nonzero(board==1)
  black_points = np.count_nonzero(board==2)
  return (white_points, black_points)

class OthelloGame:

  board = None
  def __init__(self, board=None):
      if board is None:
          self.board = create_new_board()
      else:
          self.board = board

  def play_move(self, posicion, jugador):
    if not check_valid_move(self.board, posicion, jugador):
        raise ValueError("Movimiento no válido")

    new_board = update_board(self.board.copy(), posicion, jugador)
    return OthelloGame(new_board)


  def get_valid_moves(self, jugador):
      return get_valid_moves(self.board, jugador)

  def has_finished(self):
     return has_finished(self.board)

  def get_results(self):
     return get_results(self.board)
  
