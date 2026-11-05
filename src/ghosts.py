from src.player_mechanics import Game
from src.pacman import PacMan
from src.pacgum import Pacgum
from pygame import Surface
import pygame as pg
import time


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
        return int(x // self.cell_size), int(y // self.cell_size)

    def find_target(self):
        t_col, t_row = self.pacman.current_cell()
        return t_col, t_row

    def distance_to_center(self, x: int, y: int, direction: int) -> float:
        col, row = self.current_cell(x, y)
        center_x, center_y = self.cell_center(col, row)
        if direction == UP:
            return y - center_y
        if direction == DOWN:
            return center_y - y
        if direction == LEFT:
            return x - center_x
        if direction == RIGHT:
            return center_x - x
        return 0

    def walk_path(self, x: int, y: int, direction: int, speed):
        if direction == 1:
            y -= speed
        elif direction == 2:
            x += speed
        elif direction == 4:
            y += speed
        elif direction == 8:
            x -= speed
        return x, y

    def convert_path_direction(self, path: list[tuple[int, int]]):
        i = 0
        j = 1
        directions = []
        while j < len(path):
            x, y = path[i]
            dx, dy = path[j]
            if dy < y:
                directions.append(UP)
            elif dy > y:
                directions.append(DOWN)
            elif dx < x:
                directions.append(LEFT)
            elif dx > x:
                directions.append(RIGHT)
            i += 1
            j += 1
        return directions

    def pathfind(self, start: tuple[int, int],
                 goal: tuple[int, int]) -> list[tuple[int, int]]:
        # bfs algorithm to find the shortest path to the target cell
        queue = [start]
        came_from: dict[tuple[int, int],
                        tuple[int, int] | None] = {start: None}
        i = 0
        while i < len(queue):
            current = queue[i]
            i += 1
            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            neighbors = self.neighbors(current[1], current[0])
            for direction in neighbors:
                if direction == UP:
                    next = (current[0], current[1] - 1)
                elif direction == RIGHT:
                    next = (current[0] + 1, current[1])
                elif direction == DOWN:
                    next = (current[0], current[1] + 1)
                elif direction == LEFT:
                    next = (current[0] - 1, current[1])
                else:
                    continue
                if next not in came_from:
                    queue.append(next)
                    came_from[next] = current
        return []

    def neighbors(self, row: int, col: int) -> list[int]:
        neighbors = []
        if self.maze[row][col] & 1 == 0:
            neighbors.append(UP)
        if self.maze[row][col] & 2 == 0:
            neighbors.append(RIGHT)
        if self.maze[row][col] & 4 == 0:
            neighbors.append(DOWN)
        if self.maze[row][col] & 8 == 0:
            neighbors.append(LEFT)
        return neighbors

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

    def _detect_coaliton(self, rect):
        if rect.colliderect(self.pacman):
            return True
        return False

    # def flee_direction(self, col: int, row: int):



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
        self.direction = 0
        self.speed = 1.2 + 10 / len(self.maze)
        self.path: list = None
        self.edible = True

    def move(self):
        if 0 <= self.distance_to_center(self.x, self.y, self.direction) < self.speed:
            self.find_target()
            self.x, self.y = self.cell_center(self.current_cell(self.x, self.y))
            path = self.pathfind(self.current_cell(self.x, self.y),
                                 self.find_target())
            path = self.convert_path_direction(path)
            self.path = path
            self.direction = path[0]
        if self.path:
            self.x, self.y = self.walk_path(self.x, self.y, self.direction, self.speed)

    def run(self):
        target_col, target_row = self.find_target()
        col, row = self.current_cell(self.x, self.y)
        dest_col = col
        dest_row = row
        if target_row <= row:
            if len(self.maze) > target_row:
                dest_row = row + 1
            else:
                dest_row = row - 1
        elif target_row >= row:
            if len(self.maze) < target_row:
                dest_row = row - 1
            else:
                dest_row = row + 1
        if target_col <= col:
            if len(self.maze[0]) > target_row:
                dest_col = col + 1
            else:
                dest_col = col - 1
        elif target_col >= col:
            if len(self.maze[0]) < target_row:
                dest_col = col - 1
            else:
                dest_col = col + 1
        if 0 <= self.distance_to_center(self.x, self.y, self.direction) < self.speed:
            self.x, self.y = self.cell_center(self.current_cell(self.x, self.y))

        if self.path:
            self.x, self.y = self.walk_path(self.x, self.y, self.direction, self.speed)

    def run_blinky(self):
        blinky = pg.Surface((10, 10))
        if not self.edible:
            self.move()
        else:
            self.run()

        rect = blinky.get_rect(center=(self.x, self.y))
        blinky.fill("red")
        self.screen.blit(blinky, rect)
