import pygame as pg
from pygame import surface
from src.asset_helper import asset_loader
# from dataclasses import dataclass

# dataclass
# class Cells:
#     y: int
#     x: int
#     walls: list[int]


class PacMan(pg.sprite.Sprite):
    def __init__(self, screen: surface, size: float):
        self.screen = screen
        self.sprite = asset_loader("Pac-Man", "right")
        self.start = False
        self.size = size

    def draw_pacman(self, x: int, y: int):
        speed = 0.1
        if self.start is False:
            self.x = x
            self.y = y
            self.direction = 0
            self.start = True
        current = 0
        # self.image = self.sprite[current]

        # pg.draw.circle(self.screen, (255, 255, 0), (self.x, self.y), self.size)

        key = pg.key.get_pressed()
        if key[pg.K_w] or key[pg.K_UP]:
            self.direction = 1
        elif key[pg.K_d] or key[pg.K_RIGHT]:
            self.direction = 2
        elif key[pg.K_s] or key[pg.K_DOWN]:
            self.direction = 4
        elif key[pg.K_a] or key[pg.K_LEFT]:
            self.direction = 8

        if self.direction == 1:
            self.y -= speed
        elif self.direction == 2:
            self.x += speed
        elif self.direction == 4:
            self.y += speed
        elif self.direction == 8:
            self.x -= speed

        return


class DrawMaze:
    def __init__(self, maze: list[list[int]]):
        self.maze = maze

    def window(self):
        pg.init()
        whidth: int = 800
        height: int = 800
        cell_size = whidth / len(self.maze)
        screen = pg.display.set_mode((whidth, height))
        pg.display.set_caption("Pac Man")
        pacman_size = 150 / len(self.maze)
        pacman = PacMan(screen, pacman_size)
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
                        pg.draw.line(screen, (100, 90, 175), (y - 3, x),
                                     (y + cell_size + 3, x), 8)
                    if cell & 2:
                        pg.draw.line(screen, (100, 90, 175),
                                     (y + cell_size, x - 3),
                                     (y + cell_size, x + cell_size + 3), 8)
                    if cell & 4:
                        pg.draw.line(screen, (100, 90, 175),
                                     (y, x + cell_size),
                                     (y + cell_size, x + cell_size), 8)
                    if cell & 8:
                        pg.draw.line(screen, (100, 90, 175),
                                     (y, x), (y, x + cell_size), 8)
                i += 1

            x = 0
            y = 0
            i = 0
            for a in range(len(self.maze)):
                for b in range(len(self.maze[i])):
                    cell = self.maze[b][a]
                    x = b * cell_size
                    y = a * cell_size
                    if cell & 1:
                        pg.draw.line(screen, (175, 170, 255), (y, x),
                                     (y + cell_size, x), 2)
                    if cell & 2:
                        pg.draw.line(screen, (175, 170, 255),
                                     (y + cell_size, x),
                                     (y + cell_size, x + cell_size), 2)
                    if cell & 4:
                        pg.draw.line(screen, (175, 170, 255),
                                     (y, x + cell_size),
                                     (y + cell_size, x + cell_size), 2)
                    if cell & 8:
                        pg.draw.line(screen, (175, 170, 255),
                                     (y, x), (y, x + cell_size), 2)
                i += 1
            pacman.draw_pacman(int((((len(self.maze) + 1) // 2) * cell_size) -
                               (cell_size / 2)),
                               int((((len(self.maze) + 1) // 2) * cell_size))
                               - (cell_size / 2))

            pg.display.flip()
    pg.quit()
