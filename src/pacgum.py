from pygame import Surface
import pygame as pg
import random
from src.pacman import PacMan


class Pacgum(pg.sprite.Sprite):
    def __init__(self,
                 screen: Surface,
                 number_pg: int,
                 number_spg: int,
                 points_pg: int,
                 points_spg: int,
                 maze: list[list[int]],
                 cell_size: int,
                 pacman: PacMan):
        super().__init__()
        self.screen = screen
        self.number_pacgum = number_pg
        self.number_superpacgum = number_spg
        self.points_pacgum = points_pg
        self.points_superpacgum = points_spg
        self.maze = maze
        self.cell_size = cell_size
        self.pacman = pacman
        self.distrinuted_pacgum = self._distribute()

    def _distribute(self):
        cells = [(x, y)
                 for y in range(len(self.maze))
                 for x in range(len(self.maze[0]))
                 if self.maze[y][x] != 15]
        chosen = random.sample(cells, min(self.number_pacgum, len(cells)))
        return {((x + 0.5) * self.cell_size, (y + 0.5) * self.cell_size)
                for x, y in chosen}


    def _detect_coaliton(self, rect):
        if rect.colliderect(self.pacman):
            return True
        return False

    def draw_pacgum(self):
        gum = pg.Surface((5, 5))
        gum_list = []
        for e in list(self.distrinuted_pacgum):
            rect = gum.get_rect(center=e)
            if self._detect_coaliton(rect):
                self.distrinuted_pacgum.remove(e)
            else:
                gum.fill((255, 255, 255))
                gum_list.append((gum, rect))
        for i in gum_list:
            g, r = i
            self.screen.blit(g, r)
