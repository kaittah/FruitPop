import random
import time

import pygame

from menu import replay_menu
from display import draw_text, redraw_window
from gameplay import COLORS, GAMEDIMENSIONS, XY, initialize_board, get_impact, clear_selection, measure_fall, fall, locate, check_limits, edit_selection

pygame.init()
pygame.display.set_caption("Fruit Pop")

FPS = 60
MIN_CHAIN = 4
FRUITS = list(COLORS.keys())
XDIM, YDIM, WIDTH, HEIGHT, MARGIN, GUTTER, WINDOW_SIZE, GAMETIME = GAMEDIMENSIONS
WIN = pygame.display.set_mode(WINDOW_SIZE)

def play_game(board, startTime):
    run = True
    clock = pygame.time.Clock()
    mouseDown = False
    prevLoc = None
    selection = []
    colTotals = [0 for _ in range(XDIM)]
    score = 0
    #cause tiles to fall down when game starts
    for r in range(YDIM):
        for c in range(XDIM):
            if random.random()>0.4:
                selection.append(board[r][c])
                colTotals[c]+=1
    measure_fall(board, XY, colTotals)
    board = fall(board, GAMEDIMENSIONS, colTotals, FRUITS)
    selection.clear()
    score = 0
    endGame = False
    fallStart = time.perf_counter()

    while run:
        if time.perf_counter() - startTime > GAMETIME:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                endGame = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False
                if len(selection)>= MIN_CHAIN or selection and selection[0].fruit == 'bomb':
                    board = clear_selection(board, GAMEDIMENSIONS, selection, FRUITS)
                    score += len(selection)**2
                else:
                    for tile in selection:
                        tile.selected = 0
                selection.clear()
                prevLoc = None
                fallStart = time.perf_counter()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
        if mouseDown:
            xPos, yPos = pygame.mouse.get_pos()
            loc = locate(xPos,yPos,board, GAMEDIMENSIONS)
            if loc and check_limits(prevLoc, loc, board):
                selection = edit_selection(selection,loc)
                prevLoc = loc
        redraw_window(WIN, GAMEDIMENSIONS, board, fallStart, startTime)
        clock.tick(FPS)
        pygame.display.update()
    return score, endGame

def main():
    run = True
    board = initialize_board(XY, FRUITS)
    redraw_window(WIN, GAMEDIMENSIONS, board)
    draw_text(WIN, 'Click to Start', 30, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
    pygame.display.update()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                run = replay_menu(board, play_game, draw_text, WIN, GAMEDIMENSIONS, FRUITS)
    pygame.quit()
    

main()   

