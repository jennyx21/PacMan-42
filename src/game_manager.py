import pygame as pg
from enum import Enum, auto
from src.highscores import HighscoreRecord, Leaderboard, NameInput
from src.menu import GameMenu
from src.drawmaze import DrawMaze, Results
from src.maze_loader import MazeLoader, MazeLoaderError
from src.parser import GameConfig
from src.asset_helper import asset_loader


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    NAME_INPUT = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
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
        # self.instruction = asset_loader()

        # resources
        self.config = config if config is not None else GameConfig()
        self.highscores = HighscoreRecord(self.config.highscore_filename)
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
            # elif self.state == GameState.INSTRUCTIONS:
            #     self._handle_instructions()
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
        level = self.config.levels[0]
        maze_data = MazeLoader.load(
            width=level.width,
            height=level.height,
            seed=self.config.seed,
        )
        game_loop = DrawMaze(
            maze=maze_data.grid,
            pacgum=self.config.pacgum,
            superpacgum=4,
            points_pg=self.config.points_per_pacgum,
            points_spg=self.config.points_per_super_pacgum,
            points_ghost=self.config.points_per_ghost,
            lives=self.config.lives,
            max_time=self.config.level_max_time,
            screen=self.screen,
            score=self.current_score,
            level=1,
        )
        result = game_loop.window(self.screen, self.clock)
        self.current_score = result.score

        if result.outcome == "QUIT":
            self.running = False
        elif result.outcome == "BACK":
            self.state = GameState.MENU
        else:
            self.state = GameState.NAME_INPUT

    def _handle_name_input(self) -> None:
        action = self.name_input.get_name(
            self.screen, self.clock, self.current_score)
        if action == "QUIT":
            self.running = False
        elif action == "BACK":
            self.state = GameState.MENU
        else:
            self.state = GameState.HIGHSCORES

    def _handle_highscores(self) -> None:
        action = self.leaderboard.display(self.screen, self.clock)
        if action == "QUIT":
            self.running = False
        else:
            self.state = GameState.MENU

    # def _handle_instructions(self) -> None:
        # action = asset_loader(self.)
        # if action == "QUIT":
        #     self.running = False
        # else:
        #     self.state = GameState.MENU


if __name__ == "__main__":
    manager = GameManager()
    manager.run()
