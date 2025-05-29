import pygame
from othello_agent import OthelloAgent
from othello import OthelloGame
import sys
class ManualOthelloAgent(OthelloAgent):
    def choose_move(self, game: OthelloGame):
        from othello_interface import TILE_SIZE, draw_board

        valid_moves = game.get_valid_moves(self.player)
        print(f"Player {self.player}, waiting for click...")

        while True:
            draw_board(game.board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    move = (row, col)
                    if move in valid_moves:
                        print(f"Player {self.player} clicked: {move}")
                        return move
                    else:
                        print(f"Invalid move clicked: {move}")
