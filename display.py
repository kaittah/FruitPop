import pygame
import time

def draw_text(game, text, size, color, x, y):
    gameFont = pygame.font.SysFont("comicsans", size, bold = True)
    label = gameFont.render(text, 1, color)
    w = label.get_width()
    h = label.get_height()
    game.WIN.blit(label, (x-w//2, y-h//2))

def redraw_window(game, fallTime = time.perf_counter(), startTime=time.perf_counter()):
    game.WIN.fill((0,0,0))
    fallingTime = time.perf_counter() - fallTime
    elapsedTime = time.perf_counter() - startTime
    for row in range(game.YDIM):
        for tile in game.board[row]:
            if tile.extraHeight>0:
                tile.extraHeight -= round(game.VEL + game.ACC*fallingTime)
                if tile.extraHeight <0:
                    tile.extraHeight = 0
                    tile.fallDist = 0
            if tile.selected:
                pygame.draw.rect(game.WIN, (255, 255, 255), [tile.x-game.MARGIN//4,
                                                        tile.y - tile.extraHeight-game.MARGIN//4,
                                                        game.WIDTH+game.MARGIN//2, game.HEIGHT+game.MARGIN//2])
            pygame.draw.rect(game.WIN, tile.get_color(), [tile.x, tile.y - tile.extraHeight,
                                                         game.WIDTH, game.HEIGHT])
    if elapsedTime <1:
        pass
    else:
        draw_text(game, f'Time Remaining: {int(game.GAMETIME - elapsedTime)}', 30, (0, 0, 255), (game.WINDOW_SIZE[0])//2, game.WINDOW_SIZE[1] - game.GUTTER//2)
        draw_text(game, f'Score: {game.score}', 20, (255, 255, 255), (game.WINDOW_SIZE[0]//2), (game.GUTTER)-20)
        if elapsedTime < 1.5:
            draw_text(game, 'Ready?!?', 60, (255,255,255), (game.WINDOW_SIZE[0])//2, (game.GUTTER)//2)
        elif elapsedTime <2.5:
            draw_text(game, 'Start!', 60, (255,255,255), (game.WINDOW_SIZE[0])//2, (game.GUTTER)//2)
        elif elapsedTime > game.GAMETIME - 1 and elapsedTime < game.GAMETIME:
            draw_text(game, 'Time\'s Up!', 60, (255,255,255), (game.WINDOW_SIZE[0])//2, (game.GUTTER)//2)
        elif elapsedTime > game.GAMETIME - 2 and elapsedTime < game.GAMETIME:
            draw_text(game, '1', 60, (255,255,255), (game.WINDOW_SIZE[0])//2, (game.GUTTER)//2)
        elif elapsedTime > game.GAMETIME - 3 and elapsedTime < game.GAMETIME:
            draw_text(game, '2', 60, (255,255,255), (game.WINDOW_SIZE[0])//2, (game.GUTTER)//2)
        elif elapsedTime > game.GAMETIME - 4 and elapsedTime < game.GAMETIME:
            draw_text(game, '3', 60, (255,255,255), (game.WINDOW_SIZE[0])//2, (game.GUTTER)//2)
        
