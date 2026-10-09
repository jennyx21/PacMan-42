import pygame as pg
from dataclasses import dataclass

@dataclass
class PacMan:


class DrawMaze:
    def __init__(self, maze: list[list[int]]):
        self.maze = maze

    def window(self):
        pg.init()
        cell_size = 50 * len(self.maze) / len(self.maze)
        whidth: int = 50 * len(self.maze)
        height: int = 50 * len(self.maze[0])
        screen = pg.display.set_mode((whidth, height))

        running = True

        while running:
            for event in pg.event.get():
                if event.type is pg.QUIT:
                    running = False
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                running = False

            screen.fill((5, 0, 25))
            x = 0
            y = 0
            i = 0
            for a in range(len(self.maze)):
                for b in range(len(self.maze[i])):
                    cell = self.maze[b][a]
                    x = b * cell_size
                    y = a * cell_size
                    if cell & 1:
                        pg.draw.line(screen, (100, 90, 175), (y, x), (y + cell_size, x), 6)
                        pg.draw.line(screen, (175, 170, 255), (y, x), (y + cell_size, x), 2)
                    if cell & 2:
                        pg.draw.line(screen, (100, 90, 175), (y + cell_size, x), (y + cell_size, x + cell_size), 6)
                        pg.draw.line(screen, (175, 170, 255), (y + cell_size, x), (y + cell_size, x + cell_size), 2)
                    if cell & 4:
                        pg.draw.line(screen, (100, 90, 175), (y, x + cell_size), (y + cell_size , x + cell_size), 6)
                        pg.draw.line(screen, (175, 170, 255), (y, x + cell_size), (y + cell_size , x + cell_size), 2)
                    if cell & 8:
                        pg.draw.line(screen, (100, 90, 175), (y, x), (y, x + cell_size), 6)
                        pg.draw.line(screen, (175, 170, 255), (y, x), (y, x + cell_size), 2)
                i += 1

            pg.display.flip()
    pg.quit()
