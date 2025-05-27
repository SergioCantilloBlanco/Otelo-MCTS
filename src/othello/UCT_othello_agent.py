import random
from math import sqrt

from node import Node
from othello_agent import OthelloAgent

from othello import OthelloGame, update_board


class RandomOthelloAgent(OthelloAgent):
  Cp = 1/sqrt(2)

  def choose_move(self, game: OthelloGame ):
       pass
    
  
  def treePolicy(self, node: Node):
       vertex  = node
       while not vertex.state.has_finished():
           if not vertex.is_fully_expanded():
               return self.expand(vertex)
           else:
               vertex = self.bestChild(vertex, self.Cp)
        
       pass

  def expand(self, parent):
        
        action = parent.unused_actions.pop(0)
        state = parent.state.play_move(action, parent.player)
        next_player =  2 if parent.player ==1 else 1
        if not state.get_valid_moves(next_player):
            next_player = parent.player
        child = Node(state,next_player,action,parent)
        parent.children.append(child)
        pass

  def bestChild(self, node: Node, c):
        pass

  def defaultPolicy(self, game: OthelloGame):
        state = game
        player = self.player
        while(not state.has_finished()):
          if not state.get_valid_moves(player):
               player = 2 if player==1 else 1
               continue
          action = random.choice(state.get_valid_moves(player))
          state.play_move(self, action,player)
          player = 2 if player==1 else 1
        results = state.get_results()

        if results[0] == results[1]:
          return 0
        winner = 1 if results[0] > results[1] else 2
        return 1 if self.player == winner else -1


  def backups():
        pass
  
  
