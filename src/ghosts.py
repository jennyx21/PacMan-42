from src.player_mechanics import Game
from src.pacman import PacMan
from src.pacgum import Pacgum
from pygame import Surface
import pygame as pg


class Ghosts(pg.sprite.Sprite):
    def __init__(self, screen: Surface,
                 game: Game,
                 maze: list[list[int]],
                 cell_size: float,):
        super().__init__()
        self.screen = screen
        self.game = game
        self.maze = maze
        self.cell_size = cell_size

    def draw_ghosts(self):
        blinky = pg.Surface((10, 10))
        blinky.fill("red")
        pinky = pg.Surface((10, 10))
        pinky.fill("pink")
        inky = pg.Surface((10, 10))
        inky.fill("blue")
        clyde = pg.Surface((10, 10))
        clyde.fill("orange")
        self.screen.blit(blinky, (0 + self.cell_size / 2, 0 + self.cell_size / 2))
        self.screen.blit(pinky, (0 + self.cell_size / 2, (len(self.maze) * self.cell_size) - (self.cell_size / 2)))
        self.screen.blit(inky, ((len(self.maze) * self.cell_size) - (self.cell_size / 2), 0 + self.cell_size / 2))
        self.screen.blit(clyde, ((len(self.maze) * self.cell_size) - (self.cell_size / 2), (len(self.maze) * self.cell_size) - (self.cell_size / 2)))