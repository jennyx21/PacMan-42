from src.player_mechanics import Game
from src.pacman import PacMan
from src.pacgum import Pacgum
from pygame import Surface
import pygame as pg


UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8

OPPOSITE = {UP: DOWN, RIGHT: LEFT, DOWN: UP, LEFT: RIGHT}


class Ghosts(pg.sprite.Sprite):
    def __init__(self, screen: Surface,
                 maze: list[list[int]],
                 cell_size: float,
                 pacman: PacMan,
                 game: Game):
        super().__init__()
        self.screen = screen
        self.maze = maze
        self.cell_size = cell_size
        self.pacman = pacman
        self.game = game
        self.edible = False
        self.pinky_start = (self.cell_size / 2,
                            (len(self.maze) * self.cell_size) -
                            (self.cell_size / 2))
        self.inky_start = ((len(self.maze) * self.cell_size) -
                           (self.cell_size / 2), 0 + self.cell_size / 2)
        self.clyde_start = ((len(self.maze) * self.cell_size) -
                            (self.cell_size / 2),
                            (len(self.maze) * self.cell_size) -
                            (self.cell_size / 2))
        # self.blinky = Blinky(screen, cell_size, maze, pacman, game)



    def cell_center(self, col: int, row: int) -> tuple[float, float]:
        return ((col + 0.5) * self.cell_size), (row + 0.5) * self.cell_size

    def current_cell(self, x: int, y: int) -> tuple[int, int]:
        return int(self.x // self.cell_size), int(self.y // self.cell_size)

    def find_target(self, x: int, y: int):
        t_col, t_row = self.pacman.current_cell()
        return t_col, t_row

    
    def distance_to_center(self, x: int, y: int):
        col, row = self.current_cell()
        center_x, center_y = self.cell_center(col, row)
        if self.direction == UP:
            return self.y - center_y
        if self.direction == DOWN:
            return center_y - self.y
        if self.direction == LEFT:
            return self.x - center_x
        if self.direction == RIGHT:
            return center_x - self.x
        return 0

    # def pathfind(self, col: int, row: int):



    def draw_ghosts(self):
        # self.blinky.run_blinky()
        pinky = pg.Surface((10, 10))
        pinky.fill("pink")
        inky = pg.Surface((10, 10))
        inky.fill("blue")
        clyde = pg.Surface((10, 10))
        clyde.fill("orange")
        # location_col, location_row = self.find_target()
        
        # self.pathfind(location_col, location_row)

        self.screen.blit(pinky, self.pinky_start)
        self.screen.blit(inky, self.inky_start)
        self.screen.blit(clyde, self.clyde_start)


class Blinky(Ghosts):
    def __init__(self,
                 surface: Surface,
                 cell_size: int,
                 maze: list[list[int]],
                 pacman: PacMan,
                 game: Game):
        super().__init__(surface,
                         maze,
                         cell_size,
                         pacman,
                         game)
        self.x = self.cell_size / 2
        self.y = self.cell_size / 2
        self.blink_start = (self.x, self.y)

    def run_blinky(self):
        self.find_target(self.x, self.y)
        
        blinky = pg.Surface((10, 10))
        blinky.fill("red")
        self.screen.blit(blinky, self.blink_start)
