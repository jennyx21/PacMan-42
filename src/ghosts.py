from src.player_mechanics import Game
from src.pacman import PacMan
from src.asset_helper import asset_loader
from pygame import Surface
import pygame as pg
import math


UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8
STOP = 0

OPPOSITE = {UP: DOWN, RIGHT: LEFT, DOWN: UP, LEFT: RIGHT, STOP: 0}


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
        clyde = pg.Surface((10, 10))
        clyde.fill("orange")
        self.screen.blit(clyde, self.clyde_start)

    def flee_direction(self, col: int, row: int, old_direction: int):
        t_col, t_row = self.find_target()
        neightbors = self.neighbors(row, col)
        if len(neightbors) == 1:
            return neightbors[0]
        if OPPOSITE[old_direction] in neightbors:
            neightbors.remove(OPPOSITE[old_direction])
        d_col = RIGHT if col >= t_col else LEFT
        d_row = DOWN if row >= t_row else UP
        if abs(row - t_row) >= abs(col - t_col):
            order = [d_row, d_col, OPPOSITE[d_row], OPPOSITE[d_col]]
        else:
            order = [d_col, d_row, OPPOSITE[d_col], OPPOSITE[d_row]]
        for d in order:
            if d in neightbors:
                return d
        return 0

    def move(self, x: int, y: int,
             direction: int, speed: int,
             target: tuple[int, int], path: list[int]):
        if 0 <= self.distance_to_center(x, y, direction) < speed:
            col, row = self.current_cell(x, y)
            x, y = self.cell_center(col, row)
            path = self.pathfind(self.current_cell(x, y), target)
            path = self.convert_path_direction(path)
            if path:
                self.direction = path[0]
            else:
                self.direction = 0
        if path:
            x, y = self.walk_path(x, y, direction, speed)
        return path, x, y

    def run(self, x: int, y: int, direction: int, speed: int):
        if 0 <= self.distance_to_center(x, y, direction) < speed:
            col, row = self.current_cell(x, y)
            x, y = self.cell_center(col, row)
            direction = self.flee_direction(col, row, direction)
        if direction:
            x, y = self.walk_path(x, y, direction, speed)
        return direction, x, y

    def _detect_coaliton_ghosts(self, rect):
        dist = math.hypot(self.x - self.pacman.x, self.y - self.pacman.y)
        return dist < self.cell_size * 0.4

    def vali_t(self, target: tuple[int, int]):
        col, row = target
        if row > len(self.maze) - 1 or row < 0 or col > len(self.maze) - 1 or col < 0:
            return self.find_target()
        if self.maze[row][col] == 15:
            return self.find_target()
        return col, row


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
        self.blinky_start = (self.x, self.y)
        self.direction = 0
        self.speed = 0.5 + 10 / len(self.maze)
        self.path: list = None
        self.edible = False
        self.edible_timer = 15000
        self.time = 0
        self.checked = 0
        self.sprite_up = asset_loader("blinky", "up", len(self.maze) / 0.5)
        self.sprite_left = asset_loader("blinky",
                                        "left", len(self.maze) / 0.5)
        self.sprite_right = asset_loader("blinky",
                                         "right", len(self.maze) / 0.5)
        self.sprite_down = asset_loader("blinky",
                                        "down", len(self.maze) / 0.5)
        self.sprite_edibleup = asset_loader("edible", "up",
                                            len(self.maze) / 0.5)
        self.sprite_edibleleft = asset_loader("edible", "left",
                                              len(self.maze) / 0.5)
        self.sprite_edibleright = asset_loader("edible", "right",
                                               len(self.maze) / 0.5)
        self.sprite_edibledown = asset_loader("edible", "down",
                                              len(self.maze) / 0.5)
        self.current = 0
        self.current_sprite = self.sprite_down

    def switch_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_up
        if self.direction == DOWN:
            self.current_sprite = self.sprite_down
        if self.direction == LEFT:
            self.current_sprite = self.sprite_left
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_right

    def switch_edible_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_edibleup
        if self.direction == DOWN:
            self.current_sprite = self.sprite_edibledown
        if self.direction == LEFT:
            self.current_sprite = self.sprite_edibleleft
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_edibleright

    def run_blinky(self):
        self
        start, pause = self.game.game_info()
        if start:
            if not pause:
                if not self.edible:
                    image = self.current_sprite[0]
                    rect = image.get_rect(center=(self.x, self.y))
                    self.speed = 1.2 + 10 / len(self.maze)
                    self.path, self.x, self.y = self.move(self.x, self.y,
                                                          self.direction,
                                                          self.speed,
                                                          self.find_target(),
                                                          self.path)
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer

                    if (self._detect_coaliton_ghosts(rect)
                            and not self.game.cheat
                            and not self.game.live_lost):
                        self.game.loose_lives()
                        row, col = self.pacman.start_cell
                        self.pacman.x, self.pacman.y = self.cell_center(row,
                                                                        col)
                        self.x, self.y = self.blinky_start
                    elif self.game.live_lost:
                        self.x, self.y = self.blinky_start
                    self.switch_sprite()
                else:
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer
                    self.switch_edible_sprite()
                    if self.time - 5000 < pg.time.get_ticks():
                        if self.current < len(self.current_sprite):
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                        else:
                            self.current = 0
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                    else:
                        image = self.current_sprite[0]
                        rect = image.get_rect(center=(self.x, self.y))
                    if self.time <= pg.time.get_ticks():
                        self.edible = False
                    self.speed = 1 + 10 / len(self.maze)
                    self.direction, self.x, self.y = self.run(self.x,
                                                              self.y,
                                                              self.direction,
                                                              self.speed)
                    if self._detect_coaliton_ghosts(rect):
                        self.x, self.y = self.blinky_start
                        self.edible = False
# hard codet Points of the ghost.. need to be changed
                        self.game.add_points(200)
                    self.current += 0.2
            else:
                image = self.current_sprite[0]
                rect = image.get_rect(center=(self.x, self.y))
        else:
            image = self.current_sprite[0]
            rect = image.get_rect(center=(self.x, self.y))
        self.checked = 0
        self.screen.blit(image, rect)


class Pinky(Ghosts):
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
        self.y = (len(self.maze) * self.cell_size) - (self.cell_size / 2)
        self.pinky_start = (self.x, self.y)
        self.direction = 0
        self.speed = 0.5 + 10 / len(self.maze)
        self.path: list = None
        self.edible = False
        self.edible_timer = 15000
        self.time = 0
        self.checked = 0
        self.sprite_up = asset_loader("pinky", "up", len(self.maze) / 0.5)
        self.sprite_left = asset_loader("pinky",
                                        "left", len(self.maze) / 0.5)
        self.sprite_right = asset_loader("pinky",
                                         "right", len(self.maze) / 0.5)
        self.sprite_down = asset_loader("pinky",
                                        "down", len(self.maze) / 0.5)
        self.sprite_edibleup = asset_loader("edible", "up",
                                            len(self.maze) / 0.5)
        self.sprite_edibleleft = asset_loader("edible", "left",
                                              len(self.maze) / 0.5)
        self.sprite_edibleright = asset_loader("edible", "right",
                                               len(self.maze) / 0.5)
        self.sprite_edibledown = asset_loader("edible", "down",
                                              len(self.maze) / 0.5)
        self.current = 0
        self.current_sprite = self.sprite_down


    def switch_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_up
        if self.direction == DOWN:
            self.current_sprite = self.sprite_down
        if self.direction == LEFT:
            self.current_sprite = self.sprite_left
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_right

    def switch_edible_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_edibleup
        if self.direction == DOWN:
            self.current_sprite = self.sprite_edibledown
        if self.direction == LEFT:
            self.current_sprite = self.sprite_edibleleft
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_edibleright

    def pinky_target(self):
        col, row = self.find_target()
        col += 2
        if col > len(self.maze):
            col -= 4
        return col, row

    def run_pinky(self):
        start, pause = self.game.game_info()
        if start:
            if not pause:
                if not self.edible:
                    image = self.current_sprite[0]
                    rect = image.get_rect(center=(self.x, self.y))
                    self.speed = 1.2 + 10 / len(self.maze)
                    t_col, t_row = self.pinky_target()
                    self.path, self.x, self.y = self.move(self.x, self.y,
                                                          self.direction,
                                                          self.speed,
                                                          self.vali_t((t_row,
                                                                      t_col)),
                                                          self.path)
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer

                    if (self._detect_coaliton_ghosts(rect)
                            and not self.game.cheat
                            and not self.game.live_lost):
                        self.game.loose_lives()
                        row, col = self.pacman.start_cell
                        self.pacman.x, self.pacman.y = self.cell_center(row,
                                                                        col)
                        self.x, self.y = self.pinky_start
                    elif self.game.live_lost:
                        self.x, self.y = self.pinky_start
                    self.switch_sprite()
                else:
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer
                    self.switch_edible_sprite()
                    if self.time - 5000 < pg.time.get_ticks():
                        if self.current < len(self.current_sprite):
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                        else:
                            self.current = 0
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                    else:
                        image = self.current_sprite[0]
                        rect = image.get_rect(center=(self.x, self.y))
                    if self.time <= pg.time.get_ticks():
                        self.edible = False
                    self.speed = 1 + 10 / len(self.maze)
                    self.direction, self.x, self.y = self.run(self.x,
                                                              self.y,
                                                              self.direction,
                                                              self.speed)
                    if self._detect_coaliton_ghosts(rect):
                        self.x, self.y = self.pinky_start
                        self.edible = False
# hard codet Points of the ghost.. need to be changed
                        self.game.add_points(200)
                    self.current += 0.2
            else:
                image = self.current_sprite[0]
                rect = image.get_rect(center=(self.x, self.y))
        else:
            image = self.current_sprite[0]
            rect = image.get_rect(center=(self.x, self.y))
        self.checked = 0
        self.screen.blit(image, rect)


class Inky(Ghosts):
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
        self.x = (len(self.maze) * self.cell_size) - (self.cell_size / 2)
        self.y = self.cell_size / 2
        self.inky_start = (self.x, self.y)
        self.direction = 0
        self.speed = 0.5 + 10 / len(self.maze)
        self.path: list = None
        self.edible = False
        self.edible_timer = 15000
        self.time = 0
        self.checked = 0
        self.sprite_up = asset_loader("inky", "up", len(self.maze) / 0.5)
        self.sprite_left = asset_loader("inky",
                                        "left", len(self.maze) / 0.5)
        self.sprite_right = asset_loader("inky",
                                         "right", len(self.maze) / 0.5)
        self.sprite_down = asset_loader("inky",
                                        "down", len(self.maze) / 0.5)
        self.sprite_edibleup = asset_loader("edible", "up",
                                            len(self.maze) / 0.5)
        self.sprite_edibleleft = asset_loader("edible", "left",
                                              len(self.maze) / 0.5)
        self.sprite_edibleright = asset_loader("edible", "right",
                                               len(self.maze) / 0.5)
        self.sprite_edibledown = asset_loader("edible", "down",
                                              len(self.maze) / 0.5)
        self.current = 0
        self.current_sprite = self.sprite_down

    def switch_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_up
        if self.direction == DOWN:
            self.current_sprite = self.sprite_down
        if self.direction == LEFT:
            self.current_sprite = self.sprite_left
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_right

    def switch_edible_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_edibleup
        if self.direction == DOWN:
            self.current_sprite = self.sprite_edibledown
        if self.direction == LEFT:
            self.current_sprite = self.sprite_edibleleft
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_edibleright

    def inky_target(self):
        col, row = self.find_target()
        row += 2
        if row > len(self.maze):
            row -= 4
        return col, row

    def run_inky(self):
        start, pause = self.game.game_info()
        if start:
            if not pause:
                if not self.edible:
                    image = self.current_sprite[0]
                    rect = image.get_rect(center=(self.x, self.y))
                    self.speed = 1.2 + 10 / len(self.maze)
                    t_col, t_row = self.inky_target()
                    self.path, self.x, self.y = self.move(self.x, self.y,
                                                          self.direction,
                                                          self.speed,
                                                          self.vali_t((t_col,
                                                                       t_row)),
                                                          self.path)
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer

                    if (self._detect_coaliton_ghosts(rect)
                            and not self.game.cheat
                            and not self.game.live_lost):
                        self.game.loose_lives()
                        row, col = self.pacman.start_cell
                        self.pacman.x, self.pacman.y = self.cell_center(row,
                                                                        col)
                        self.x, self.y = self.inky_start
                    elif self.game.live_lost:
                        self.x, self.y = self.inky_start
                    self.switch_sprite()
                else:
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer
                    self.switch_edible_sprite()
                    if self.time - 5000 < pg.time.get_ticks():
                        if self.current < len(self.current_sprite):
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                        else:
                            self.current = 0
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                    else:
                        image = self.current_sprite[0]
                        rect = image.get_rect(center=(self.x, self.y))
                    if self.time <= pg.time.get_ticks():
                        self.edible = False
                    self.speed = 1 + 10 / len(self.maze)
                    self.direction, self.x, self.y = self.run(self.x,
                                                              self.y,
                                                              self.direction,
                                                              self.speed)
                    if self._detect_coaliton_ghosts(rect):
                        self.x, self.y = self.inky_start
                        self.edible = False
# hard codet Points of the ghost.. need to be changed
                        self.game.add_points(200)
                    self.current += 0.2
            else:
                image = self.current_sprite[0]
                rect = image.get_rect(center=(self.x, self.y))
        else:
            image = self.current_sprite[0]
            rect = image.get_rect(center=(self.x, self.y))
        self.checked = 0
        self.screen.blit(image, rect)


class Clyde(Ghosts):
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
        self.x = (len(self.maze) * self.cell_size) - (self.cell_size / 2)
        self.y = (len(self.maze) * self.cell_size) - (self.cell_size / 2)
        self.clyde_start = (self.x, self.y)
        self.direction = 0
        self.speed = 0.5 + 10 / len(self.maze)
        self.path: list = None
        self.edible = False
        self.edible_timer = 15000
        self.time = 0
        self.checked = 0
        self.sprite_up = asset_loader("clyde", "up", len(self.maze) / 0.5)
        self.sprite_left = asset_loader("clyde",
                                        "left", len(self.maze) / 0.5)
        self.sprite_right = asset_loader("clyde",
                                         "right", len(self.maze) / 0.5)
        self.sprite_down = asset_loader("clyde",
                                        "down", len(self.maze) / 0.5)
        self.sprite_edibleup = asset_loader("edible", "up",
                                            len(self.maze) / 0.5)
        self.sprite_edibleleft = asset_loader("edible", "left",
                                              len(self.maze) / 0.5)
        self.sprite_edibleright = asset_loader("edible", "right",
                                               len(self.maze) / 0.5)
        self.sprite_edibledown = asset_loader("edible", "down",
                                              len(self.maze) / 0.5)
        self.current = 0
        self.current_sprite = self.sprite_down

    def switch_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_up
        if self.direction == DOWN:
            self.current_sprite = self.sprite_down
        if self.direction == LEFT:
            self.current_sprite = self.sprite_left
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_right

    def switch_edible_sprite(self):
        if self.direction == UP:
            self.current_sprite = self.sprite_edibleup
        if self.direction == DOWN:
            self.current_sprite = self.sprite_edibledown
        if self.direction == LEFT:
            self.current_sprite = self.sprite_edibleleft
        if self.direction == RIGHT:
            self.current_sprite = self.sprite_edibleright

    def clyde_target(self):
        col, row = self.find_target()
        c_col, c_row = self.current_cell(self.x, self.y)
        if abs(row - c_row) < 5 or abs(col - c_col) < 5:
            row = len(self.maze)
            col = len(self.maze)
        return col, row


    def run_clyde(self):
        start, pause = self.game.game_info()
        if start:
            if not pause:
                if not self.edible:
                    image = self.current_sprite[0]
                    rect = image.get_rect(center=(self.x, self.y))
                    self.speed = 1.2 + 10 / len(self.maze)
                    t_col, t_row = self.clyde_target()
                    self.path, self.x, self.y = self.move(self.x, self.y,
                                                          self.direction,
                                                          self.speed,
                                                          self.vali_t((t_col,
                                                                       t_row)),
                                                          self.path)
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer

                    if (self._detect_coaliton_ghosts(rect)
                            and not self.game.cheat
                            and not self.game.live_lost):
                        self.game.loose_lives()
                        row, col = self.pacman.start_cell
                        self.pacman.x, self.pacman.y = self.cell_center(row,
                                                                        col)
                        self.x, self.y = self.clyde_start
                    elif self.game.live_lost:
                        self.x, self.y = self.clyde_start

                    self.switch_sprite()
                else:
                    if self.game.signal and self.checked == 0:
                        self.edible = True
                        self.checked = 1
                        self.time = pg.time.get_ticks() + self.edible_timer
                    self.switch_edible_sprite()
                    if self.time - 5000 < pg.time.get_ticks():
                        if self.current < len(self.current_sprite):
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                        else:
                            self.current = 0
                            image = self.current_sprite[int(self.current)]
                            rect = image.get_rect(center=(self.x, self.y))
                    else:
                        image = self.current_sprite[0]
                        rect = image.get_rect(center=(self.x, self.y))
                    if self.time <= pg.time.get_ticks():
                        self.edible = False
                    self.speed = 1 + 10 / len(self.maze)
                    self.direction, self.x, self.y = self.run(self.x,
                                                              self.y,
                                                              self.direction,
                                                              self.speed)
                    if self._detect_coaliton_ghosts(rect):
                        self.x, self.y = self.clyde_start
                        self.edible = False
# hard codet Points of the ghost.. need to be changed
                        self.game.add_points(200)
                    self.current += 0.2
            else:
                image = self.current_sprite[0]
                rect = image.get_rect(center=(self.x, self.y))
        else:
            image = self.current_sprite[0]
            rect = image.get_rect(center=(self.x, self.y))
        self.checked = 0
        self.screen.blit(image, rect)
