import tkinter as tk
import sqlite3
import pygame
import time

from gameplay import initialize_board

class EnterButton(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text = 'Enter username', command = self.on_button)
        self.button.pack(side = tk.RIGHT)
        self.entry.pack(side = tk.LEFT)
        self.username = ''
    def on_button(self):
        self.username = self.entry.get()
        self.entry
        tk.Tk.destroy(self)

def replay_menu(board, play_game, draw_text, WIN, GAMEDIMENSIONS, FRUITS):
    fruitpop_db = "fruitpop_db.db"
    conn = sqlite3.connect(fruitpop_db)
    c = conn.cursor()
    XDIM, YDIM, WIDTH, HEIGHT, MARGIN, GUTTER, WINDOW_SIZE, GAMETIME = GAMEDIMENSIONS
    endGame = False
    while endGame == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endGame = True
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                startTime = time.perf_counter()
                score, endGame = play_game(board, startTime)
                if endGame:
                    return False
                board = initialize_board([XDIM,YDIM], FRUITS)
                button = EnterButton()
                button.mainloop() 
                username = button.username
                try:
                    c.execute('''INSERT into score_table VALUES (?, ?);''', (username, score))
                    conn.commit()
                    draw_text(WIN, 'Click to Replay', 30, (255,255,255), (WINDOW_SIZE[0])//2, (GUTTER)//2)
                    things = c.execute('''SELECT * FROM score_table ORDER BY score DESC LIMIT 5;''').fetchall()
                    conn.commit()
                    r = 0
                    draw_text(WIN, 'High Scores:', 40, (255, 255, 255), (WINDOW_SIZE[0])//2, (GUTTER*2))
                    for row in things:
                      r +=1
                      draw_text(WIN, f'{row[0]}....{row[1]}', 30, (255,255,255),(WINDOW_SIZE[0])//2, (GUTTER*2 + 30*r))
                except:
                    print("must create score table by running create_db.py")
                pygame.display.update()
    conn.close()
    return False
