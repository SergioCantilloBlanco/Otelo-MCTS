import random
from math import inf, log, sqrt

from node import Node
from othello_agent import OthelloAgent

from othello import OthelloGame, update_board


class UCTOtelloAgent(OthelloAgent):
  Cp = 1/sqrt(2)

  def choose_move(self, game: OthelloGame ):
      root = Node(game, self.player )
      n = 10
      for i in range(n):
          #print(f"Iteration {i+1}/{n}")
          vl = self.tree_policy(root)
          delta = self.default_policy(vl.state, vl.player)
          self.backup_negamax(vl, delta)
      return self.best_child(root,0).previous_action


  def tree_policy(self, node: Node):
       vertex  = node
       while not vertex.state.has_finished():
           if not vertex.is_fully_expanded():
               return self.expand(vertex)
           else:
               vertex = self.best_child(vertex, self.Cp)

       return vertex

  def expand(self, parent):

        action = parent.unused_actions.pop(0)
        state = parent.state.play_move(action, parent.player)
        next_player =  2 if parent.player == 1 else 1
        if not state.get_valid_moves(next_player):
            next_player = parent.player
        child = Node(state,next_player,action,parent)
        parent.children.append(child)
        #print(f"Expanding {parent} using action {action} to child {child}")
        return child

  def best_child(self, node: Node, c):
        bestChild=None
        maxValue= -inf
        for child in node.children:
            value = child.accumulated_rewards/child.visits + c* sqrt((2*log(node.visits))/child.visits)
            if value > maxValue:
                maxValue = value
                bestChild = child

        return bestChild

  def default_policy(self, game: OthelloGame, player):
        state = OthelloGame(game.board.copy())
        while(not state.has_finished()):
          if not state.get_valid_moves(player):
               player = 2 if player==1 else 1
               continue
          action = random.choice(state.get_valid_moves(player))
          state = state.play_move(action,player)
          #print(f"Player {player} played action {action}")
          #print(state.board)
          player = 2 if player==1 else 1
        results = state.get_results()

        if results[0] == results[1]:
          return 0
        winner = 1 if results[0] > results[1] else 2
        return 1 if self.player == winner else -1


  def backup_negamax(self, node: Node, delta):
        node_to_propagate = node
        while node_to_propagate != None:
            node_to_propagate.visits += 1
            node_to_propagate.accumulated_rewards += delta
            if node_to_propagate.parent is not None and node_to_propagate.player != node_to_propagate.parent.player:
              delta = -delta
            node_to_propagate = node_to_propagate.parent
