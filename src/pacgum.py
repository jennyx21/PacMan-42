from pygame import Surface
import pygame as pg
import random
from src.pacman import PacMan
from src.player_mechanics import Game


class Pacgum(pg.sprite.Sprite):
    def __init__(self,
                 screen: Surface,
                 number_pg: int,
                 number_spg: int,
                 points_pg: int,
                 points_spg: int,
                 maze: list[list[int]],
                 cell_size: int,
                 pacman: PacMan,
                 game: Game):
        super().__init__()
        self.screen = screen
        self.number_pacgum = number_pg
        self.number_superpacgum = number_spg
        self.points_pacgum = points_pg
        self.points_superpacgum = points_spg
        self.maze = maze
        self.cell_size = cell_size
        self.pacman = pacman
        self.game = game
        self.timer = 0
        self.distributed_pacgum = self._distribute()
        self.distribute_superpacgum = self._distribute_super()

    def _distribute(self):
        cells = [(x, y)
                 for y in range(len(self.maze))
                 for x in range(len(self.maze[0]))
                 if self.maze[y][x] != 15]
        chosen = random.sample(cells, min(self.number_pacgum, len(cells)))
        return {((x + 0.5) * self.cell_size, (y + 0.5) * self.cell_size)
                for x, y in chosen}

    def _distribute_super(self):
        cell = []
        cell.append((0.5 * self.cell_size, 0.5 * self.cell_size))
        cell.append((len(self.maze) * self.cell_size - 0.5 * self.cell_size,
                    0.5 * self.cell_size))
        cell.append((len(self.maze) * self.cell_size - 0.5 * self.cell_size,
                     len(self.maze) * self.cell_size - 0.5 * self.cell_size))
        cell.append((0.5 * self.cell_size,
                    len(self.maze) * self.cell_size - 0.5 * self.cell_size))
        return cell

    def _detect_coaliton(self, rect):
        if rect.colliderect(self.pacman):
            return True
        return False

    def draw_pacgum(self):
        gum = pg.Surface((5, 5))
        gum_list = []
        for e in list(self.distributed_pacgum):
            rect = gum.get_rect(center=e)
            if self._detect_coaliton(rect):
                self.distributed_pacgum.remove(e)
                self.game.add_points(self.points_pacgum)
            else:
                gum.fill((255, 255, 255))
                gum_list.append((gum, rect))
        for i in gum_list:
            g, r = i
            self.screen.blit(g, r)

    def signal_return(self):
        current_tic = pg.time.get_ticks()
        if current_tic > self.timer:
            self.game.reset_signal()
        return

    def draw_superpacgum(self):
        supergum = pg.Surface((10, 10))
        super_gum_list = []
        if self.game.signal:
            self.signal_return()
        for e in self.distribute_superpacgum:
            super_rect = supergum.get_rect(center=e)
            if self._detect_coaliton(super_rect):
                self.game.give_signal()
                time = pg.time.get_ticks()
                self.timer = time + 20
                self.game.add_points(self.points_superpacgum)
                self.distribute_superpacgum.remove(e)
            else:
                supergum.fill("white")
                super_gum_list.append((supergum, super_rect))
        for i in super_gum_list:
            g, r = i
            self.screen.blit(g, r)

    def run_gums(self):
        self.draw_pacgum()
        self.draw_superpacgum()
