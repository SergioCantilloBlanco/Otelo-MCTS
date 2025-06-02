import numpy as np
import copy

directions = [(1,0), (-1,0), (0,1), (0,-1) , (1,1) , (1,-1), (-1,1) ,(-1,-1)]

def create_new_board():
    board = np.zeros((8,8),dtype=int)
    search_set = [[(3,3),(4,4)],[(4,3),(3,4)]]

    board[3,3] = 1
    board[4,4] = 1
    board[4,3] = 2
    board[3,4] = 2
    return board, search_set

def get_valid_moves(board, conjunto,  player):

    valid_moves = []

    conj = copy.deepcopy(conjunto)

    search_set = list(conj[0] if player == 2 else conj[1])

    remove_list= []

    for tile in search_set:
      is_enclosed = True
      for direction in directions:
        row, column = tile
        row_direction, column_direction = direction
        looking_row, looking_column = (row  + row_direction , column + column_direction)
        if (0 <= looking_row <= 7 and 0 <= looking_column <= 7):
          if board[looking_row, looking_column] == 0:
              is_enclosed = False
              if not (looking_row,looking_column) in  valid_moves:
                opposite_direction = (row_direction * -1 , column_direction * -1)
                if check_valid_move_in_direction(board, (looking_row,looking_column), player, opposite_direction):
                    valid_moves.append((looking_row,looking_column))
      if is_enclosed:
        remove_list.append(tile)

    for i in remove_list:
        search_set.remove(i)

    new_search_set = [list(conj[0]), list(conj[1])]
    new_search_set[0 if player == 2 else 1] = search_set
    return valid_moves, new_search_set



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

def update_board(board, search_set, position, player):
      fila,columna = position
      board[fila,columna] = player

      search_set[0 if player == 1 else 1].append(position)

      for direccion in directions:
        board, search_set = update_line(board.copy(), copy.deepcopy(search_set), position, player, direccion)


      return board, search_set


def update_line(board, search_set, position, player, direction):
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

                search_set[0 if player == 1 else 1].append((row_to_invert, column_to_invert))

                if (row_to_invert, column_to_invert) in search_set[1 if player == 1 else 0]:
                  search_set[1 if player == 1 else 0].remove((row_to_invert, column_to_invert))

            keep_searching = False
    return board,search_set


def has_finished(board, search_set):
   mov_1, ss  = get_valid_moves(board, copy.deepcopy(search_set),1)
   mov_2, ss  = get_valid_moves(board,copy.deepcopy(ss), 2)
   return len(mov_1) + len(mov_2) == 0 ,ss

def get_results(board):
  white_points = np.count_nonzero(board==1)
  black_points = np.count_nonzero(board==2)

  return (white_points, black_points)

class OthelloGame:

  board = None
  search_set= None
  def __init__(self, board=None, search_set=None):
      if board is None:
          self.board, self.search_set = create_new_board()
      else:
          self.board = board
          if search_set == None:
            raise ReferenceError("Non updated search set")
          self.search_set = copy.deepcopy(search_set)


  def play_move(self, posicion, jugador):
    new_board, search_set = update_board(self.board.copy(),copy.deepcopy(self.search_set), posicion, jugador)
    return OthelloGame(new_board, search_set)


  def get_valid_moves(self, jugador):
      valid_moves, search_set =  get_valid_moves(self.board, self.search_set, jugador)
      self.search_set = copy.deepcopy(search_set)
      return valid_moves

  def has_finished(self):
     res, search_set =  has_finished(self.board, self.search_set)
     self.search_set = search_set
     return res

  def get_results(self):
     return get_results(self.board)
