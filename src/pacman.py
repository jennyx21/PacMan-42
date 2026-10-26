import pygame as pg
from pygame import surface
from src.player_mechanics import Game
from src.asset_helper import asset_loader


class PacMan(pg.sprite.Sprite, Game):
    def __init__(self, screen: surface, game: Game):
        super().__init__()
        self.screen = screen
        self.game = game
        self.sprite_right = asset_loader("Pac-Man", "right")
        self.sprite_down = asset_loader("Pac-Man", "down")
        self.sprite_left = asset_loader("Pac-Man", "left")
        self.sprite_up = asset_loader("Pac-Man", "up")
        self.current_sprite = self.sprite_right
        self.start = False
        self.current = 0

    def draw_pacman(self, x: int, y: int):
        speed = 1.2
        key = pg.key.get_pressed()
        self.start = self.game.game_info()
        if self.start is False:
            self.x = x
            self.y = y
            self.direction = 0
            self.image = self.current_sprite[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

        if self.start is True:
            if self.current < len(self.current_sprite):
                self.image = self.current_sprite[int(self.current)]
            else:
                self.current = 0
                self.image = self.current_sprite[int(self.current)]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

            if key[pg.K_w] or key[pg.K_UP]:
                self.direction = 1
                self.current_sprite = self.sprite_up
            elif key[pg.K_d] or key[pg.K_RIGHT]:
                self.direction = 2
                self.current_sprite = self.sprite_right
            elif key[pg.K_s] or key[pg.K_DOWN]:
                self.direction = 4
                self.current_sprite = self.sprite_down
            elif key[pg.K_a] or key[pg.K_LEFT]:
                self.direction = 8
                self.current_sprite = self.sprite_left

            if self.direction == 1:
                self.y -= speed
            elif self.direction == 2:
                self.x += speed
            elif self.direction == 4:
                self.y += speed
            elif self.direction == 8:
                self.x -= speed

            self.current += 0.3
        self.screen.blit(self.image, self.rect)
