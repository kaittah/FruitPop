class Tile:
    def __init__(self, game, row, column, fruit):
        self.game = game
        self.x = (game.MARGIN + game.WIDTH)* column + game.GUTTER
        self.y = (game.MARGIN + game.HEIGHT)* row + game.GUTTER
        self.column = column
        self.filled = 1
        self.fruit = fruit
        self.fallDist = 0
        self.selected = 0
        self.extraHeight = 0
    def get_row(self):
        return ((self.y - self.game.GUTTER)//(self.game.MARGIN + self.game.HEIGHT))
    def set_y(self, row):
        self.y = (self.game.MARGIN + self.game.HEIGHT)* row + self.game.GUTTER
    def get_color(self):
        return self.game.COLORS[self.fruit]