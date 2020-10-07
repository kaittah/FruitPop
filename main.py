import random
import time

import pygame

from menu import replay_menu
from display import draw_text, redraw_window
from gameplay import COLORS, GAMEDIMENSIONS, XY, initialize_board, get_impact, clear_selection, measure_fall, fall, locate, check_limits, edit_selection
from play_game import play_game, WIN
from play_ai_game import play_ai_game

pygame.init()
pygame.display.set_caption("Fruit Pop")
FRUITS = list(COLORS.keys())
XDIM, YDIM, WIDTH, HEIGHT, MARGIN, GUTTER, WINDOW_SIZE, GAMETIME = GAMEDIMENSIONS

def main():
    run = True
    board = initialize_board(XY, FRUITS)
    redraw_window(WIN, GAMEDIMENSIONS, board)
    draw_text(WIN, 'Click here to Start', 50, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
    draw_text(WIN, 'Click here for Autopilot', 40, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2 + 60)
    pygame.display.update()
    
    while run:
        for event in pygame.event.get():
            xPos, yPos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if yPos > GUTTER//2 + 40:
                    run = replay_menu(board, play_ai_game, draw_text, WIN, GAMEDIMENSIONS, FRUITS)
                else:
                    run = replay_menu(board, play_game, draw_text, WIN, GAMEDIMENSIONS, FRUITS)
    pygame.quit()
    

main()   

