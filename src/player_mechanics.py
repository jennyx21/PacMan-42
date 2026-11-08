import time
import pygame as pg
from pygame import Surface
from src.asset_helper import asset_loader


class Game():
    def __init__(self, screen: Surface, highscore: int, lives: int):
        self.start = False
        self.pause = False
        self.highscore = highscore
        self.signal = 0
        self.index = 0
        self.pacman_lives = lives
        self.live_list: list = self.rameining_lives()
        self.screen = screen

        self.live_on_spirete = asset_loader("lives", "on", 20)
        self.live_off_spirete = asset_loader("lives", "off", 20)

    def rameining_lives(self):
        lives = []
        for i in range(self.pacman_lives):
            lives.append(1)
        while len(lives) < 3:
            lives.append(0)
        lives.reverse()
        return lives

    def add_points(self, points: int):
        self.highscore += points

    def game_info(self) -> tuple[bool, bool]:
        return self.start, self.pause

    def update_start(self) -> None:
        if self.start is False:
            self.start = True
        elif self.start is True and self.pause is False:
            self.pause = True
        elif self.start is True and self.pause is True:
            self.pause = False
        time.sleep(0.2)

    def give_signal(self):
        self.signal = 1

    def reset_signal(self):
        self.signal = 0

    def update_edibility(self, edible_state: bool):
        if edible_state is False:
            return True
        else:
            return False

    def display_highscore(self):
        pg.font.init()
        font = pg.font.SysFont("arial", 30)
        text = font.render(f"SCORE: {str(self.highscore)}", True, "white")
        self.screen.blit(text, (10, 10))

    def loose_lives(self):
        self.pacman_lives -= 1
        self.live_list[self.live_list.index(1)] = 0

    def diplay_lives(self):
        x = 700
        y = 25
        for live in self.live_list:
            if live == 1:
                image = self.live_on_spirete[0]
                rect = image.get_rect(center=(x, y))
            else:
                image = self.live_off_spirete[0]
                rect = image.get_rect(center=(x, y))
            x += 33
            self.screen.blit(image, rect)

    def lives_info(self):
        return self.pacman_lives
