import pygame as pg
from enum import Enum, auto
from src.highscores import HighscoreRecord, Leaderboard, NameInput
from src.menu import GameMenu
from src.drawmaze import DrawMaze
from src.maze_loader import MazeLoader, MazeLoaderError
from src.parser import GameConfig
from pathlib import Path


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    NAME_INPUT = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    QUIT = auto()


class GameManager:
    def __init__(self, config: GameConfig | None = None,
                 width: int = 800, height: int = 800) -> None:
        # pygame
        pg.init()
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption("Pac-Man")
        self.clock = pg.time.Clock()

        # menu
        self.config = config if config is not None else GameConfig()
        self.highscores = HighscoreRecord(self.config.highscore_filename)
        self.leaderboard = Leaderboard(self.highscores)
        self.name_input = NameInput(self.highscores)
        self.menu = GameMenu(self.screen, self.highscores)

        # current
        self.state = GameState.MENU
        self.current_score = 0
        self.current_lives = self.config.lives
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
            elif self.state == GameState.INSTRUCTIONS:
                self._handle_instructions()
            elif self.state == GameState.QUIT:
                self.running = False

        pg.quit()

    def _handle_menu(self) -> None:
        action = self.menu.run()
        if action == "PLAY":
            self.state = GameState.PLAYING
        elif action == "HIGHSCORES":
            self.state = GameState.HIGHSCORES
        elif action == "INSTRUCTION":
            self.state = GameState.INSTRUCTIONS
        else:
            self.state = GameState.QUIT

    def _show_end_screen(self, outcome: str, score: int) -> str:
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font_pause = pg.font.Font(None, 64)
        font_sub = pg.font.Font(None, 28)

        title = "GAME OVER" if outcome == "LOSE" else "YOU WIN!"
        color = (255, 60, 60) if outcome == "LOSE" else (60, 255, 60)
        over_surf = font_pause.render(title, True, color)
        self.screen.blit(
            over_surf,
            over_surf.get_rect(
                center=(self.width // 2, self.height // 2 - 30)),
        )

        score_surf = font_sub.render(
            f"FINAL SCORE: {score}", True, (255, 255, 0))
        self.screen.blit(
            score_surf,
            score_surf.get_rect(
                center=(self.width // 2, self.height // 2 + 20)),
        )

        prompt_surf = font_sub.render(
            "PRESS ANY KEY TO CONTINUE...", True, (200, 200, 200)
        )
        self.screen.blit(
            prompt_surf,
            prompt_surf.get_rect(
                center=(self.width // 2, self.height // 2 + 65)),
        )

        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "QUIT"
                elif event.type == pg.KEYDOWN:
                    waiting = False
            self.clock.tick(60)
        return "CONTINUE"

    def _show_level_cleared_screen(self, level_num: int, score: int) -> str:
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font_pause = pg.font.Font(None, 64)
        font_sub = pg.font.Font(None, 28)

        over_surf = font_pause.render(
            f"LEVEL {level_num} CLEARED!", True, (60, 255, 60))
        self.screen.blit(
            over_surf,
            over_surf.get_rect(
                center=(self.width // 2, self.height // 2 - 30)),
        )

        score_surf = font_sub.render(
            f"CURRENT SCORE: {score}", True, (255, 255, 0))
        self.screen.blit(
            score_surf,
            score_surf.get_rect(
                center=(self.width // 2, self.height // 2 + 20)),
        )

        prompt_surf = font_sub.render(
            "PRESS ANY KEY FOR NEXT LEVEL...", True, (200, 200, 200)
        )
        self.screen.blit(
            prompt_surf,
            prompt_surf.get_rect(
                center=(self.width // 2, self.height // 2 + 65)),
        )

        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "QUIT"
                elif event.type == pg.KEYDOWN:
                    waiting = False
            self.clock.tick(60)
        return "CONTINUE"

    def _handle_playing(self) -> None:
        self.current_score = 0
        lives = self.config.lives

        for idx, level_cfg in enumerate(self.config.levels):
            try:
                maze_data = MazeLoader.load(
                    width=level_cfg.width,
                    height=level_cfg.height,
                    seed=self.config.seed + idx,
                )
            except MazeLoaderError as e:
                print(f"MazeLoaderError: {e}")
                self.state = GameState.MENU
                return

            game_loop = DrawMaze(
                maze=maze_data.grid,
                pacgum=self.config.pacgum,
                superpacgum=4,
                points_pg=self.config.points_per_pacgum,
                points_spg=self.config.points_per_super_pacgum,
                points_ghost=self.config.points_per_ghost,
                lives=lives,
                max_time=self.config.level_max_time,
                screen=self.screen,
                score=self.current_score,
                level=level_cfg.level if hasattr(
                    level_cfg, "level") else (idx + 1),
            )
            result = game_loop.window(self.screen, self.clock)
            self.current_score = result.score
            lives = result.lives

            if result.outcome == "QUIT":
                self.running = False
                return
            elif result.outcome == "BACK":
                self.state = GameState.MENU
                return
            elif result.outcome == "LOSE":
                action = self._show_end_screen("LOSE", self.current_score)
                if action == "QUIT":
                    self.running = False
                else:
                    self.state = GameState.NAME_INPUT
                return
            elif result.outcome == "WIN":
                is_last_level = (idx == len(self.config.levels) - 1)
                if is_last_level:
                    action = self._show_end_screen("WIN", self.current_score)
                    if action == "QUIT":
                        self.running = False
                    else:
                        self.state = GameState.NAME_INPUT
                    return
                else:
                    action = self._show_level_cleared_screen(
                        idx + 1, self.current_score)
                    if action == "QUIT":
                        self.running = False
                        return

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

    def _handle_instructions(self) -> None:
        asset_dir = Path("src/assets/instruction_assets")
        instructions = pg.image.load(asset_dir, "instruction")
        rules = pg.image.load(asset_dir, "rules")
        self.screen.blit(instructions, (0, 0))
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                action = "QUIT"
            if event.type == pg.KEYDOWN:
                self.screen.blit(rules, (0, 0))
        if action == "QUIT":
            self.running = False
        else:
            self.state = GameState.MENU


if __name__ == "__main__":
    manager = GameManager()
    manager.run()
