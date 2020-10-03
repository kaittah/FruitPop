import pygame
import time

VEL = 0
ACC = 4

def draw_text(surface, text, size, color, x, y):
    gameFont = pygame.font.SysFont("comicsans", size, bold = True)
    label = gameFont.render(text, 1, color)
    w = label.get_width()
    h = label.get_height()
    surface.blit(label, (x-w//2, y-h//2))

def redraw_window(surface, GAMEDIMENSIONS, board, fallTime = time.perf_counter(), startTime=time.perf_counter()):
    XDIM, YDIM, WIDTH, HEIGHT, MARGIN, GUTTER, WINDOW_SIZE, GAMETIME = GAMEDIMENSIONS
    surface.fill((0,0,0))
    fallingTime = time.perf_counter() - fallTime
    elapsedTime = time.perf_counter() - startTime
    for row in range(YDIM):
        for tile in board[row]:
            if tile.extraHeight>0:
                tile.extraHeight -= round(VEL + ACC*fallingTime)
                if tile.extraHeight <0:
                    tile.extraHeight = 0
                    tile.fallDist = 0
            if tile.selected:
                pygame.draw.rect(surface, (255, 255, 255), [tile.x-MARGIN//4,
                                                        tile.y - tile.extraHeight-MARGIN//4,
                                                        WIDTH+MARGIN//2, HEIGHT+MARGIN//2])
            pygame.draw.rect(surface, tile.get_color(), [tile.x, tile.y - tile.extraHeight,
                                                         WIDTH, HEIGHT])
    if elapsedTime <1:
        pass
    else:
        draw_text(surface, f'Time Remaining: {int(GAMETIME - elapsedTime)}', 30, (0, 0, 255), (WINDOW_SIZE[0])//2, WINDOW_SIZE[1] - GUTTER//2)
        if elapsedTime < 1.5:
            draw_text(surface, 'Ready?!?', 60, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
        elif elapsedTime <2.5:
            draw_text(surface, 'Start!', 60, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
        elif elapsedTime > GAMETIME - 1 and elapsedTime < GAMETIME:
            draw_text(surface, 'Time\'s Up!', 60, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
        elif elapsedTime > GAMETIME - 2 and elapsedTime < GAMETIME:
            draw_text(surface, '1', 60, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
        elif elapsedTime > GAMETIME - 3 and elapsedTime < GAMETIME:
            draw_text(surface, '2', 60, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
        elif elapsedTime > GAMETIME - 4 and elapsedTime < GAMETIME:
            draw_text(surface, '3', 60, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
