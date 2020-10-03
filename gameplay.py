import pygame
import random
import time

#GAME CONSTANTS
XDIM = 8
YDIM = 10
WIDTH, HEIGHT = (45,45)
MARGIN, GUTTER = (5, 100)
WINDOW_SIZE = [(WIDTH + MARGIN)*XDIM + 2*GUTTER, (HEIGHT + MARGIN)*YDIM + 2*GUTTER]
GAMETIME = 30
BOMBR = 2
WEIGHTS = [10,10,10,10,1,1,0]

XY = [XDIM, YDIM]
GAMEDIMENSIONS = [XDIM, YDIM, WIDTH, HEIGHT, MARGIN, GUTTER, WINDOW_SIZE, GAMETIME]

COLORS = {
        'cherry': (255,80,80),
        'watermelon': (153, 255, 153),
        'orange': (255, 153, 51),
        'blueberry': (0, 153, 255),
        'wild': (153, 51, 255),
        'bomb': (51, 51, 153),
        'detonated': (51, 51, 153)
        }

class Tile:
    def __init__(self, row, column, fruit):
        self.x = (MARGIN + WIDTH)* column + GUTTER
        self.y = (MARGIN + HEIGHT)* row + GUTTER
        self.column = column
        self.filled = 1
        self.fruit = fruit
        self.fallDist = 0
        self.selected = 0
        self.extraHeight = 0
    def get_row(self):
        return ((self.y - GUTTER)//(MARGIN + HEIGHT))
    def set_y(self, row):
        self.y = (MARGIN + HEIGHT)* row + GUTTER
    def get_color(self):
        return COLORS[self.fruit]

def initialize_board(XY, FRUITS):
    XDIM, YDIM = XY
    randomBoard = []
    for row in range(YDIM):
        randomBoard.append([])
        for column in range(XDIM):
            randomFruit = random.choices(FRUITS, weights= WEIGHTS, k = 1)[0]
            randomBoard[row].append(Tile(row, column, randomFruit))
    return randomBoard

def get_impact(board, XY, selected, impactArea = set()):
    #return set of tiles to be cleared
    XDIM, YDIM = XY
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
            for y in range(max(0, bomb.get_row() - BOMBR), min(bomb.get_row() + 1 + BOMBR, YDIM)):
                for x in range(max(0, bomb.column - BOMBR), min(bomb.column + 1 + BOMBR, XDIM)):
                    if (x-bomb.column)**2 + (y-bomb.get_row())**2 <= BOMBR**2:
                        poof.add(board[y][x])
            bomb.fruit = 'detonated'
            get_impact(board, XY, poof, impactArea)
    return impactArea

def measure_fall(board, XY, colTotals):
    #associate a board location with number of rows a tile will fall to get there
    XDIM, YDIM = XY
    for column in range(XDIM):
        for row in range(YDIM-1, -1, -1):
            voidCount = 0
            while voidCount < colTotals[column] and board[row-voidCount][column].filled ==0:
                voidCount +=1
            board[row][column].fallDist = voidCount
            if row-voidCount >-1:
                board[row-voidCount][column].filled = 0
            if voidCount == colTotals[column]:
                for r in range(row-1, -1, -1):
                    board[r][column].fallDist = voidCount
                break

def fall(board, GAMEDIMENSIONS, colTotals, FRUITS):
    #move tile instances down on the board
    XDIM, YDIM, _, HEIGHT, MARGIN, _, _ , _ = GAMEDIMENSIONS
    newBoard = []
    for row in range(YDIM):
        newBoard.append([])
        for column in range(XDIM):
            newBoard[row].append(None)
    for c in range(XDIM):
        colTot = colTotals[c]
        for r in range(colTot):
            newBoard[r][c] = Tile(r, c, random.choices(FRUITS, weights = WEIGHTS, k=1)[0])
            newBoard[r][c].extraHeight = colTot*(HEIGHT+MARGIN)
        for r2 in range(colTot,YDIM):
            distance = board[r2][c].fallDist
            newBoard[r2][c] = board[r2-distance][c]
            newBoard[r2][c].extraHeight = distance*(HEIGHT+MARGIN)
            newBoard[r2][c].filled = 1
            newBoard[r2][c].set_y(r2)
    return newBoard

def clear_selection(board, GAMEDIMENSIONS, selection, FRUITS):
    xy = GAMEDIMENSIONS[0:2]
    colTotals = [0 for _ in range(XDIM)]
    impactArea = get_impact(board, xy, set(selection), set())
    for tile in impactArea:
        tile.filled = 0
        colTotals[tile.column] +=1
        tile.selected = 0
    measure_fall(board, xy, colTotals)
    board = fall(board, GAMEDIMENSIONS, colTotals, FRUITS)
    return board
    
def locate(x,y, board, GAMEDIMENSIONS):
    XDIM, YDIM, WIDTH, HEIGHT, MARGIN, GUTTER, _ , _ = GAMEDIMENSIONS
    row = (y-GUTTER)//(WIDTH+MARGIN)
    column = (x-GUTTER)//(HEIGHT+MARGIN)
    if row < YDIM and row >-1 and column < XDIM and column >-1:
        return board[row][column]
    else:
        return None

def check_limits(prevLoc, tile, board):
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
