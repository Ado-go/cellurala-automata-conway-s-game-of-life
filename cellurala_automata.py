import tkinter as tk

Width = 500
Height = 500

root = tk.Tk()
root.title("Automat game, Generation: 0")

canvas = tk.Canvas(width=Width, height=Height)
canvas.pack()


class Game:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tiles = 50
        self.tile_size = Width // self.tiles
        self.speed = 1
        self.generation = 0
        self.running = False
        self.field = [[False for _ in range(self.tiles)] for _ in range(self.tiles)]
        self.draw_field()

    def restart(self, _):
        self.x = self.x
        self.y = self.y
        self.tiles = self.tiles
        self.speed = self.speed
        self.generation = 0
        self.tile_size = self.tile_size
        self.running = False
        self.field = [[False for _ in range(self.tiles)] for _ in range(self.tiles)]
        canvas.delete("all")
        self.draw_field()
        root.title("Automat game, Generation: 0")

    def draw_field(self):
        col_space = self.y
        for row in self.field:
            row_space = self.x
            for _ in row:
                canvas.create_rectangle(row_space, col_space,
                                        row_space + self.tile_size, col_space + self.tile_size,
                                        fill="white", tags=str(col_space) + str(row_space) + "on")
                canvas.create_rectangle(row_space, col_space,
                                        row_space + self.tile_size, col_space + self.tile_size,
                                        fill="gray", tags=str(col_space) + str(row_space) + "off")
                row_space += self.tile_size
            col_space += self.tile_size

    def make_on_off(self, event):
        if event.num == 1 or event.state == 264:
            change = True
        else:
            change = False
        col = ((event.x - self.x) // self.tile_size)
        row = ((event.y - self.y) // self.tile_size)
        if self.tiles - 2 >= row >= 1 and self.tiles - 2 >= col >= 1:
            if self.field[row][col] != change:
                if self.field[row][col]:
                    self.field[row][col] = not self.field[row][col]
                    canvas.tag_lower(str(row * self.tile_size)+str(col * self.tile_size) +
                                     "on", str(row * self.tile_size)+str(col*self.tile_size)+"off")
                else:
                    self.field[row][col] = not self.field[row][col]
                    canvas.tag_lower(str(row * self.tile_size) + str(col*self.tile_size)
                                     + "off", str(row*self.tile_size) + str(col * self.tile_size) + "on")

    def on_off(self):
        self.generation += 1
        root.title("Automat game, Generation: {}".format(self.generation))
        new_field = [[False for _ in range(self.tiles)] for _ in range(self.tiles)]
        for x in range(1, self.tiles-1):
            for y in range(1, self.tiles-1):
                neighbours = 0
                for i in range(-1, 2, 1):
                    for j in range(-1, 2, 1):
                        if self.field[x+i][y+j]:
                            neighbours += 1
                if self.field[x][y]:
                    neighbours -= 1
                if self.field[x][y] and (neighbours < 2 or neighbours > 3):
                    new_field[x][y] = not self.field[x][y]
                elif not self.field[x][y] and neighbours == 3:
                    new_field[x][y] = not self.field[x][y]
                else:
                    new_field[x][y] = self.field[x][y]
        for i in range(1, self.tiles-1):
            for j in range(1, self.tiles-1):
                if self.field[i][j] != new_field[i][j]:
                    if new_field[i][j]:
                        canvas.tag_lower(str(i * self.tile_size) + str(j * self.tile_size) +
                                         "off", str(i * self.tile_size) + str(j * self.tile_size) + "on")
                    else:
                        canvas.tag_lower(str(i * self.tile_size) + str(j * self.tile_size) +
                                         "on", str(i * self.tile_size) + str(j * self.tile_size) + "off")
        self.field = new_field

    def start(self, _):
        self.running = not self.running

    def update(self):
        if self.running:
            self.on_off()
        canvas.after(self.speed, self.update)


game = Game(0, 0)

canvas.bind("<Button-1>", game.make_on_off)
canvas.bind("<B1-Motion>", game.make_on_off)
canvas.bind("<Button-3>", game.make_on_off)
canvas.bind("<B3-Motion>", game.make_on_off)
canvas.bind_all("s", game.start)
canvas.bind_all("r", game.restart)
canvas.after(game.speed, game.update)
canvas.mainloop()
