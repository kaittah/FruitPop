import random
import time

import pygame

from display import draw_text, redraw_window
from game import Game
from menu import idle, display_scores

def main():
    pygame.init()
    pygame.display.set_caption("Fruit Pop")
    run = True
    game_played = False
    while run:
        if game_played:
            display_scores(g)
        g = Game()
        if not game_played:
            redraw_window(g)
        draw_text(g, 'Click here to Start', 50, (255,255,255), (g.WINDOW_SIZE[0])//2, (g.GUTTER)//2)
        draw_text(g, 'Click here for Autopilot', 40, (255,255,255), (g.WINDOW_SIZE[0])//2, (g.GUTTER)//2 + 60)
        pygame.display.update()

        ai_setting = idle(g)
        if ai_setting == 'QUIT':
            run = False
        else:
            run = g.play(ai_setting)
            game_played = True
            
        
    pygame.quit()
    

main()   

