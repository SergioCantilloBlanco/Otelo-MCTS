import random
from math import inf, log, sqrt

from node import Node
from othello_agent import OthelloAgent

from othello import OthelloGame, update_board


class UCTOtelloAgent(OthelloAgent):
  Cp = 1/sqrt(2)

  def __init__(self, player, n=10):
    self.player = player
    self.n = n

  def choose_move(self, game: OthelloGame ):
      root = Node(game, self.player )
      for i in range(self.n):
          # print(f"Iteration {i+1}/{n}")
          vl = self.tree_policy(root)
          delta = self.default_policy(vl.state, vl.player)
          self.backup_negamax(vl, delta)
      return self.best_child(root,0).previous_action


  def tree_policy(self, node: Node):
       vertex = node
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
        child = Node(state,next_player,action,parent)
        parent.children.append(child)
        # print(f"Expanding {parent} using action {action} to child {child}")

        if not child.unused_actions and not child.state.has_finished():
            second_next_player =  2 if child.player == 1 else 1
            second_child = Node(state, second_next_player, None, child)
            child.children.append(second_child)
            return second_child

        return child

  def best_child(self, node: Node, c):
        bestChild=None
        maxValue= -inf
        precalc_2_log_node_visits = (2*log(node.visits))
        for child in node.children:
            value = child.accumulated_rewards/child.visits + c * sqrt(precalc_2_log_node_visits/child.visits)
            if value > maxValue:
                maxValue = value
                bestChild = child

        return bestChild

  def default_policy(self, game: OthelloGame, player):
      state = OthelloGame(game.board, game.search_set)
      current_player = player  # Keep track of the player for this simulation

      while(not state.has_finished()):
          valid_moves = state.get_valid_moves(current_player)
          if not valid_moves:
              current_player = 2 if current_player == 1 else 1
              continue
          action = random.choice(valid_moves)
          state = state.play_move(action, current_player)
          current_player = 2 if current_player == 1 else 1

      results = state.get_results()
      if results[0] == results[1]:
          return 0
      winner = 1 if results[0] > results[1] else 2

      return 1 if player == winner else -1


  def backup_negamax(self, node: Node, delta):
        node_to_propagate = node
        current_delta = -delta
        while node_to_propagate != None:
            node_to_propagate.visits += 1
            node_to_propagate.accumulated_rewards += current_delta
            node_to_propagate = node_to_propagate.parent
            current_delta = -current_delta
