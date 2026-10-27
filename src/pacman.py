import pygame as pg
from pygame import Surface
from src.player_mechanics import Game
from src.asset_helper import asset_loader

STOP = 0
UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8

OPPOSITE = {UP: DOWN, RIGHT: LEFT, DOWN: UP, LEFT: RIGHT, 0: STOP}


class PacMan(pg.sprite.Sprite, Game):
    def __init__(self, screen: Surface,
                 game: Game,
                 maze: list[list[int]],
                 cell_size: float,
                 start_cell: tuple[int, int]):
        super().__init__()
        self.screen = screen
        self.game = game
        self.maze = maze
        self.cell_size = cell_size
        self.sprite_right = asset_loader("Pac-Man", "right")
        self.sprite_down = asset_loader("Pac-Man", "down")
        self.sprite_left = asset_loader("Pac-Man", "left")
        self.sprite_up = asset_loader("Pac-Man", "up")

        self.current_sprite = self.sprite_right
        self.current = 0
        self.col, self.row = start_cell
        self.x, self.y = self.cell_center(self.col, self.row)
        self.direction = 0
        self.next_direction = 0

    def cell_center(self, col: int, row: int) -> tuple[float, float]:
        return ((col + 0.5) * self.cell_size), (row + 0.5) * self.cell_size

    def current_cell(self) -> tuple[int, int]:
        return int(self.x // self.cell_size), int(self.y // self.cell_size)

    def read_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.next_direction = UP
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.next_direction = RIGHT
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            self.next_direction = DOWN
        elif keys[pg.K_a] or keys[pg.K_LEFT]:
            self.next_direction = LEFT

    def update_sprite(self, direction: int):
        if direction == UP:
            self.current_sprite = self.sprite_up
        elif direction == RIGHT:
            self.current_sprite = self.sprite_right
        elif direction == DOWN:
            self.current_sprite = self.sprite_down
        elif direction == LEFT:
            self.current_sprite = self.sprite_left

    def can_move(self, direction: int) -> bool:
        x, y = self.current_cell()
        if self.maze[y][x] & direction == 0:
            return True
        return False

    def distance_to_center(self):
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

    def draw_pacman(self, x: int, y: int):
        speed = 1.2
        start, pause = self.game.game_info()
        if start is False:
            self.image = self.current_sprite[0]
            self.rect = self.image.get_rect()
            self.rect.center = (round(self.x), round(self.y))

        if start is True and pause is False:
            self.read_keys()
            if self.current < len(self.current_sprite):
                self.image = self.current_sprite[int(self.current)]
            else:
                self.current = 0
                self.image = self.current_sprite[int(self.current)]
            self.rect = self.image.get_rect()
            self.rect.center = (round(self.x), round(self.y))


            if self.next_direction == OPPOSITE[self.direction]:
                self.direction = self.next_direction

            if 0 <= self.distance_to_center() < speed:
                col, row = self.current_cell()
                self.x, self.y = self.cell_center(col, row)
                if self.can_move(self.next_direction):
                    self.direction = self.next_direction
                if not self.can_move(self.direction):
                    self.direction = 0

            if self.direction == 1:
                self.y -= speed
            elif self.direction == 2:
                self.x += speed
            elif self.direction == 4:
                self.y += speed
            elif self.direction == 8:
                self.x -= speed

            self.current += 0.2
        self.update_sprite(self.direction)
        self.screen.blit(self.image, self.rect)
