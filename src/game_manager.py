import pygame as pg
from enum import Enum, auto
from src.highscores import HighscoreRecord, Leaderboard, NameInput
from src.menu import GameMenu
# import DrawMaze
# import GameLevel


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    NAME_INPUT = auto()
    HIGHSCORES = auto()
    QUIT = auto()


class GameManager:
    def __init__(self, config=None, width: int = 800, height: int = 800) -> None:
        # pygame
        pg.init()
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption("Pac-Man")
        self.clock = pg.time.Clock()

        # menu
        self.menu = GameMenu(self.screen)

        # resources
        self.config = config
        self.highscores = HighscoreRecord("highscores.json")
        self.leaderboard = Leaderboard(self.highscores)
        self.name_input = NameInput(self.highscores)

        # current
        self.state = GameState.MENU
        self.current_score = 0
        self.running = True

    def run(self) -> None:
        """Central loop delegating to state handlers."""
        while self.running:
            if self.state == GameState.MENU:
                self._handle_menu()
            elif self.state == GameState.PLAYING:
                self._handle_playing()
            elif self.state == GameState.NAME_INPUT:
                self._handle_name_input()
            elif self.state == GameState.HIGHSCORES:
                self._handle_highscores()
            elif self.state == GameState.QUIT:
                self.running = False

        pg.quit()

    def _handle_menu(self) -> None:
        action = self.menu.run()
        if action == "PLAY":
            self.state = GameState.PLAYING
        elif action == "HIGHSCORES":
            self.state = GameState.HIGHSCORES
        else:
            self.state = GameState.QUIT

    def _handle_playing(self) -> None:
        # run game loop on self.screen
        # when game ends (death / win):
        # self.current_score = final_score
        # self.state = GameState.NAME_INPUT
        pass

    def _handle_name_input(self) -> None:
        action = self.name_input.get_name()
        if action == "QUIT":
            self.running = False
        else:
            self.state = GameState.HIGHSCORES

    def _handle_highscores(self) -> None:
        action = self.leaderboard.display(self.screen, self.clock)
        if action == "QUIT":
            self.running = False
        else:
            self.state = GameState.MENU


if __name__ == "__main__":
    manager = GameManager()
    manager.run()
