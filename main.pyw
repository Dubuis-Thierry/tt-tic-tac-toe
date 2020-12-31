import pygame, sys

import drawer
import fonts, colors
from board import PygameBoard
from button import Button

from debuglogger import DebugLogger

pygame.init()

screen = pygame.display.set_mode(size=(550, 625))
pygame.display.set_caption("TT Tic Tac Toe")


board = PygameBoard(screen, rect=(25, 100, 500, 500), dimensions=3, ai=False)


restart_button = Button(
    screen, "Restart", colors.DARK_RED, fg_color=colors.WHITE,
    callback=board.reset_cells, font=fonts.NORMAL_FONT, position=(275, 50)
)

ai_button = Button(
    screen, "AI", colors.DARK_RED, fg_color=colors.WHITE,
    callback=board.ai_move, font=fonts.NORMAL_FONT, position=(60, 50)
)

game_objects = [board, restart_button, ai_button]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DebugLogger.log("Game exit")
            sys.exit()

    screen.fill((50, 50, 50))

    for go in game_objects:
        go.pygame_update()
        
    pygame.display.flip()
