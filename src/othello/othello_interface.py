# othello_visual.py
import pygame
import sys

TILE_SIZE = 80
BOARD_SIZE = 8
SCREEN_SIZE = TILE_SIZE * BOARD_SIZE
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
GREY = (128, 128, 128)

_initialized = False
_screen = None

def draw_board(board, valid_moves=None):
    global _initialized, _screen

    if not _initialized:
        pygame.init()
        _screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Othello")
        _initialized = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    _screen.fill(GREEN)

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(_screen, LINE_COLOR, rect, 1)

            piece = board[y][x]
            if piece == 1:
                pygame.draw.circle(_screen, WHITE, rect.center, TILE_SIZE // 2 - 5)
            elif piece == 2:
                pygame.draw.circle(_screen, BLACK, rect.center, TILE_SIZE // 2 - 5)

    if valid_moves:
        for y, x in valid_moves:  # Corrected: row (y), col (x)
            center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.circle(_screen, GREY, center, TILE_SIZE // 6)

    pygame.display.flip()
