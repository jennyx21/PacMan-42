import pygame as pg
from pygame import Surface
from src.player_mechanics import Game
from src.pacman import PacMan
from src.pacgum import Pacgum


class DrawMaze:
    def __init__(self, maze: list[list[int]],
                 pacgum: int,
                 superpacgum: int,
                 points_pg: int,
                 points_spg: int):
        self.maze = maze
        self.pacgum = pacgum
        self.superpacgum = superpacgum
        self.points_pacgum = points_pg
        self.points_super_pacgum = points_spg

    def window(self):
        pg.init()
        clock = pg.time.Clock()
        whidth: int = 800
        height: int = 800
        cell_size = whidth / len(self.maze)
        middle = len(self.maze) / 2
        screen = pg.display.set_mode((whidth, height))
        pg.display.set_caption("Pac Man")
        game = Game()
        pacman = PacMan(screen,
                        game,
                        self.maze,
                        cell_size,
                        (int(middle), int(middle)))
        pacgum = Pacgum(screen,
                        self.pacgum,
                        self.superpacgum,
                        self.points_pacgum,
                        self.points_super_pacgum,
                        self.maze,
                        cell_size,
                        pacman)
        running = True

        while running:
            for event in pg.event.get():
                if event.type is pg.QUIT:
                    running = False

            start, pause = game.game_info()
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                running = False
            if keys[pg.K_SPACE] or keys[pg.K_KP_ENTER]:
                if start is not True:
                    game.update_start()
                elif start is True:
                    game.update_start()

            screen.fill((5, 0, 25))
            self.draw_walls(cell_size, screen, (100, 90, 175), 8, 3)
            self.draw_walls(cell_size, screen, (175, 170, 255), 3)

            pacman.draw_pacman(int(middle * cell_size),
                               int(middle * cell_size))
            pacgum.draw_pacgum()

            pg.display.flip()
            clock.tick(60)
        pg.quit()

    def draw_walls(self,
                   cell_size: float,
                   screen: Surface,
                   color: tuple[int, int, int],
                   size: int,
                   length: int = 0):
        x: float = 0
        y: float = 0
        i: int = 0
        for a in range(len(self.maze)):
            for b in range(len(self.maze[i])):
                cell = self.maze[b][a]
                x = b * cell_size
                y = a * cell_size
                if cell & 1:
                    pg.draw.line(screen, color, (y - length, x),
                                 (y + cell_size + length, x), size)
                if cell & 2:
                    pg.draw.line(screen, color,
                                 (y + cell_size, x - length),
                                 (y + cell_size, x + cell_size + length), size)
                if cell & 4:
                    pg.draw.line(screen, color,
                                 (y, x + cell_size),
                                 (y + cell_size, x + cell_size), size)
                if cell & 8:
                    pg.draw.line(screen, color,
                                 (y, x), (y, x + cell_size), size)
            i += 1
        return
