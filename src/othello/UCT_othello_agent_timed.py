import random
import time
from math import inf, log, sqrt

from node import Node
from othello_agent import OthelloAgent
from othello import OthelloGame


class UCTOtelloAgentTimed(OthelloAgent):
    Cp = 1 / sqrt(2)

    def choose_move(self, game: OthelloGame):
        total_start = time.perf_counter()

        root = Node(game, self.player)
        n = 200

        # Timing accumulators
        tree_time = 0
        default_time = 0
        backup_time = 0

        for i in range(n):
            iter_start = time.perf_counter()

            t1 = time.perf_counter()
            vl = self.tree_policy(root)
            t2 = time.perf_counter()
            tree_time += t2 - t1

            t1 = time.perf_counter()
            delta = self.default_policy(vl.state, vl.player)
            t2 = time.perf_counter()
            default_time += t2 - t1

            t1 = time.perf_counter()
            self.backup_negamax(vl, delta)
            t2 = time.perf_counter()
            backup_time += t2 - t1

            iter_end = time.perf_counter()
            print(f"Iteration {i+1} time: {iter_end - iter_start:.6f}s")

        move = self.best_child(root, 0).previous_action
        total_end = time.perf_counter()

        print(f"\nUCT summary for player {self.player}:")
        print(f"  Total choose_move time: {total_end - total_start:.6f}s")
        print(f"  Tree policy total time:  {tree_time:.6f}s")
        print(f"  Default policy time:     {default_time:.6f}s")
        print(f"  Backup phase time:       {backup_time:.6f}s")
        print()

        return move

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
        next_player = 2 if parent.player == 1 else 1
        if not state.get_valid_moves(next_player):
            next_player = parent.player
        child = Node(state, next_player, action, parent)
        parent.children.append(child)
        return child

    def best_child(self, node: Node, c):
        bestChild = None
        maxValue = -inf
        for child in node.children:
            value = child.accumulated_rewards / child.visits + c * sqrt((2 * log(node.visits)) / child.visits)
            if value > maxValue:
                maxValue = value
                bestChild = child
        return bestChild

    def default_policy(self, game: OthelloGame, player):
      import time

      state = OthelloGame(game.board.copy())

      has_finished_time = 0
      get_valid_time = 0
      random_choice_time = 0
      play_move_time = 0
      loop_iterations = 0

      while not state.has_finished():
          loop_iterations += 1

          # Time get_valid_moves
          t1 = time.perf_counter()
          valid_moves = state.get_valid_moves(player)
          t2 = time.perf_counter()
          get_valid_time += t2 - t1

          if not valid_moves:
              player = 2 if player == 1 else 1
              continue

          # Time random.choice
          t1 = time.perf_counter()
          action = random.choice(valid_moves)
          t2 = time.perf_counter()
          random_choice_time += t2 - t1

          # Time play_move
          t1 = time.perf_counter()
          state = state.play_move(action, player)
          t2 = time.perf_counter()
          play_move_time += t2 - t1

          player = 2 if player == 1 else 1

      results = state.get_results()
      if results[0] == results[1]:
          outcome = 0
      else:
          winner = 1 if results[0] > results[1] else 2
          outcome = 1 if self.player == winner else -1

      # Report timing
      print(f"    [default_policy stats] Iterations: {loop_iterations}")
      print(f"      get_valid_moves time: {get_valid_time:.6f}s")
      print(f"      random.choice time:   {random_choice_time:.6f}s")
      print(f"      play_move time:       {play_move_time:.6f}s")
      print(f"      avg iteration time:   {(get_valid_time + random_choice_time + play_move_time)/loop_iterations:.6f}s")

      return outcome


    def backup_negamax(self, node: Node, delta):
        node_to_propagate = node
        while node_to_propagate is not None:
            node_to_propagate.visits += 1
            node_to_propagate.accumulated_rewards += delta
            if node_to_propagate.parent is not None and node_to_propagate.player != node_to_propagate.parent.player:
                delta = -delta
            node_to_propagate = node_to_propagate.parent
