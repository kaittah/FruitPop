import tkinter as tk
import sqlite3
import time

import pygame

from display import draw_text

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

def idle(game):
    run = True
    while run:
        for event in pygame.event.get():
            xPos, yPos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                return 'QUIT'
            elif event.type == pygame.MOUSEBUTTONUP:
                if yPos > game.GUTTER//2 + 40:
                    return True
                else:
                    return False

def display_scores(game):
    fruitpop_db = "fruitpop_db.db"
    conn = sqlite3.connect(fruitpop_db)
    c = conn.cursor()
    button = EnterButton()
    button.mainloop() 
    username = button.username
    c.execute('''CREATE TABLE IF NOT EXISTS score_table (name text, score int);''')
    c.execute('''INSERT into score_table VALUES (?, ?);''', (username, game.score))
    conn.commit()
    things = c.execute('''SELECT * FROM score_table ORDER BY score DESC LIMIT 5;''').fetchall()
    conn.commit()
    r = 0
    draw_text(game, 'High Scores:', 40, (255, 255, 255), (game.WINDOW_SIZE[0])//2, (game.GUTTER*2))
    for row in things:
        r +=1
        draw_text(game, f'{row[0]}....{row[1]}', 30, (255,255,255),(game.WINDOW_SIZE[0])//2, (game.GUTTER*2 + 30*r))
    conn.close()
    return False
