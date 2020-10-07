import random
import time

import pygame

from display import draw_text, redraw_window
from gameplay import COLORS, GAMEDIMENSIONS, XY, initialize_board, get_impact, clear_selection, measure_fall, fall, locate, check_limits, edit_selection

FPS = 60
MIN_CHAIN = 4
FRUITS = list(COLORS.keys())
XDIM, YDIM, WIDTH, HEIGHT, MARGIN, GUTTER, WINDOW_SIZE, GAMETIME = GAMEDIMENSIONS
WIN = pygame.display.set_mode(WINDOW_SIZE)
TIMEBUFFER = .5 #seconds required between moves

def play_ai_game(board, startTime):
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
    chain_end = True
    fallStart = time.perf_counter()
    timesincemove = time.perf_counter() + 1

    while run:
        if time.perf_counter() - startTime > GAMETIME:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                endGame = True
        if chain_end:
            chain_end = False
            if len(selection)>= MIN_CHAIN or selection and selection[0].fruit == 'bomb':
                board = clear_selection(board, GAMEDIMENSIONS, selection, FRUITS)
                score += len(selection)**2
            else:
                for tile in selection:
                    tile.selected = 0
            selection.clear()
            rand_x = random.randrange(XDIM)
            rand_y = random.randrange(YDIM)
            prevLoc = board[rand_y][rand_x]
            selection = edit_selection(selection,prevLoc)
            fallStart = time.perf_counter()
        if time.perf_counter() - timesincemove > TIMEBUFFER:
        
            #if there is an unselected neighbor of the same color, select that one 
            c = prevLoc.column-1
            possible_move = False
            while c < prevLoc.column+2 and c < XDIM and not possible_move:
                r = prevLoc.get_row()-1
                while r < prevLoc.get_row()+2 and r < YDIM and not possible_move:
                    loc = board[r][c]
                    if check_limits(prevLoc, loc, board) and loc not in selection:
                        selection = edit_selection(selection,loc)
                        prevLoc = loc
                        possible_move = True
                        break
                    r +=1
                c +=1                    
            if not possible_move: #end the chain when there are no possible moves
                chain_end = True
            timesincemove = time.perf_counter()

        redraw_window(WIN, GAMEDIMENSIONS, board, fallStart, startTime)
        clock.tick(FPS)
        pygame.display.update()
    return score, endGame