import random
import time

import pygame

from display import redraw_window, draw_text
from tile import Tile


class Game:
    
    COLORS = {
        'cherry': (255,80,80),
        'watermelon': (153, 255, 153),
        'orange': (255, 153, 51),
        'blueberry': (0, 153, 255),
        'wild': (153, 51, 255),
        'bomb': (51, 51, 153),
        'detonated': (51, 51, 153)
        }
    FRUITS = list(COLORS.keys())
    WEIGHTS = [10,10,10,10,1,1,0]
    XDIM = 8
    YDIM = 10
    WIDTH, HEIGHT = (45,45)
    MARGIN, GUTTER = (5, 100)
    WINDOW_SIZE = [(WIDTH + MARGIN)*XDIM + 2*GUTTER, (HEIGHT + MARGIN)*YDIM + 2*GUTTER]
    GAMETIME = 30
    BOMBR = 2
    MIN_CHAIN = 4
    FPS = 60
    WIN = pygame.display.set_mode(WINDOW_SIZE)
    VEL = 0
    ACC = 4
    TIMEBUFFER = .2

    def __init__(self):
        self.board = self.initialize_board()
        self.score = 0
    
    def play(self, ai):
        run = True
        startTime = time.perf_counter()
        clock = pygame.time.Clock()
        mouseDown = False
        prevLoc = None
        selection = []
        colTotals = [0 for _ in range(self.XDIM)]
        #cause tiles to fall down when game starts
        for r in range(self.YDIM):
            for c in range(self.XDIM):
                if random.random()>0.4:
                    selection.append(self.board[r][c])  #randomly clear 60% of tiles
                    colTotals[c]+=1
        self.measure_fall(colTotals)
        self.board = self.fall(colTotals)
        selection.clear()
        chain_end = True
        fallStart = time.perf_counter()
        timesincemove = time.perf_counter() + 2
        #start gameplay
        while run:
            if time.perf_counter() - startTime > self.GAMETIME:
                run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not ai:
                        mouseDown = False
                        if len(selection)>= self.MIN_CHAIN or selection and selection[0].fruit == 'bomb':
                            self.clear_selection(selection)
                            self.score += len(selection)**2
                        else:
                            for tile in selection:
                                tile.selected = 0
                        selection.clear()
                        prevLoc = None
                        fallStart = time.perf_counter()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseDown = True
            if ai:
                if chain_end:
                    chain_end = False
                    if len(selection)>= self.MIN_CHAIN or selection and selection[0].fruit == 'bomb':
                        self.clear_selection(selection)
                        self.score += len(selection)**2
                    else:
                        for tile in selection:
                            tile.selected = 0
                    selection.clear()
                    rand_x = random.randrange(self.XDIM)
                    rand_y = random.randrange(self.YDIM)
                    prevLoc = self.board[rand_y][rand_x]
                    selection = self.edit_selection(selection,prevLoc)
                    fallStart = time.perf_counter()
                if time.perf_counter() - timesincemove > self.TIMEBUFFER:
                    #if there is an unselected neighbor of the same color, select that one 
                    c = prevLoc.column-1
                    possible_move = False
                    while c < prevLoc.column+2 and c < self.XDIM and not possible_move:
                        r = prevLoc.get_row()-1
                        while r < prevLoc.get_row()+2 and r < self.YDIM and not possible_move:
                            loc = self.board[r][c]
                            if self.check_limits(prevLoc, loc) and loc not in selection:
                                selection = self.edit_selection(selection,loc)
                                prevLoc = loc
                                possible_move = True
                                break
                            r +=1
                        c +=1                    
                    if not possible_move: #end the chain when there are no possible moves
                        chain_end = True
                    timesincemove = time.perf_counter()

            elif mouseDown and not ai:
                xPos, yPos = pygame.mouse.get_pos()
                loc = self.locate(xPos,yPos)
                if loc and self.check_limits(prevLoc, loc):
                    selection = self.edit_selection(selection,loc)
                    prevLoc = loc
            redraw_window(self, fallStart, startTime)
            clock.tick(self.FPS)
            pygame.display.update()  
        return True     

    def initialize_board(self):
        randomBoard = []
        for row in range(self.YDIM):
            randomBoard.append([])
            for column in range(self.XDIM):
                randomFruit = random.choices(self.FRUITS, weights= self.WEIGHTS, k = 1)[0]
                randomBoard[row].append(Tile(self, row, column, randomFruit))
        return randomBoard
    
    def get_impact(self, selected, impactArea = set()):
        '''
        Return a set of tiles to be cleared
        '''
        impactArea.update(selected)
        bombs = []
        for tile in selected:
            if tile.fruit == 'bomb':
                bombs.append(tile)
        if not bombs:
            return impactArea
        else:
            for bomb in bombs:
                poof = set()
                for y in range(max(0, bomb.get_row() - self.BOMBR), min(bomb.get_row() + 1 + self.BOMBR, self.YDIM)):
                    for x in range(max(0, bomb.column - self.BOMBR), min(bomb.column + 1 + self.BOMBR, self.XDIM)):
                        if (x-bomb.column)**2 + (y-bomb.get_row())**2 <= self.BOMBR**2:
                            poof.add(self.board[y][x])
                bomb.fruit = 'detonated'
                self.get_impact(poof, impactArea)
        return impactArea

    def measure_fall(self, colTotals):
        '''
        Associate a board location with number of rows a tile will fall to get there
        '''
        for column in range(self.XDIM):
            for row in range(self.YDIM-1, -1, -1):
                voidCount = 0
                while voidCount < colTotals[column] and self.board[row-voidCount][column].filled ==0:
                    voidCount +=1
                self.board[row][column].fallDist = voidCount
                if row-voidCount >-1:
                    self.board[row-voidCount][column].filled = 0
                if voidCount == colTotals[column]:
                    for r in range(row-1, -1, -1):
                        self.board[r][column].fallDist = voidCount
                    break
    def fall(self, colTotals):
        '''
        move tile instances down on the board
        '''
        newBoard = []
        for row in range(self.YDIM):
            newBoard.append([])
            for column in range(self.XDIM):
                newBoard[row].append(None)
        for c in range(self.XDIM):
            colTot = colTotals[c]
            for r in range(colTot):
                newBoard[r][c] = Tile(self, r, c, random.choices(self.FRUITS, weights = self.WEIGHTS, k=1)[0])
                newBoard[r][c].extraHeight = colTot*(self.HEIGHT+ self.MARGIN)
            for r2 in range(colTot,self.YDIM):
                distance = self.board[r2][c].fallDist
                newBoard[r2][c] = self.board[r2-distance][c]
                newBoard[r2][c].extraHeight = distance*(self.HEIGHT+self.MARGIN)
                newBoard[r2][c].filled = 1
                newBoard[r2][c].set_y(r2)
        return newBoard

    def clear_selection(self, selection):
        colTotals = [0 for _ in range(self.XDIM)]
        impactArea = self.get_impact(set(selection), set())
        for tile in impactArea:
            tile.filled = 0
            colTotals[tile.column] +=1
            tile.selected = 0
        self.measure_fall(colTotals)
        self.board = self.fall(colTotals)
    
    def locate(self, x,y):
        row = (y-self.GUTTER)//(self.WIDTH+self.MARGIN)
        column = (x-self.GUTTER)//(self.HEIGHT+self.MARGIN)
        if row < self.YDIM and row >-1 and column < self.XDIM and column >-1:
            return self.board[row][column]
        else:
            return None
    @staticmethod
    def check_limits(prevLoc, tile):
        '''
        Return true if the tile is able to be selected based on game rules
        '''
        if not prevLoc: #first selected
            return True
        elif tile == prevLoc:
            return False
        else:
            maxRow = prevLoc.get_row() +1
            minRow = maxRow -2
            maxCol= prevLoc.column + 1
            minCol = maxCol - 2
            row = tile.get_row()
            column = tile.column
        if row > maxRow or row < minRow or column > maxCol or column < minCol:
            return False
        elif tile.fruit == prevLoc.fruit:
            return True
        elif tile.fruit == 'wild' or prevLoc.fruit == 'wild':
            return True
        else:
            return False

    @staticmethod
    def edit_selection(selection,tile):
        newSelection = selection.copy()
        if tile.selected:
            i = selection.index(tile)
            newSelection = selection[:i+1]
            for unselect in selection[i+1:]:
                unselect.selected = 0
        else:
            newSelection.append(tile)
            tile.selected = 1
        return newSelection

    
