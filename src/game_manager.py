import pygame as pg
from enum import Enum, auto
from src.highscores import HighscoreRecord
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
    def __init__(self, config=None, width: int = 800, height: int = 800):
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

        # current
        self.state = GameState.MENU
        self.current_score = 0
        self.running = True

    def run(self):
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

    def _handle_menu(self):
        action = self.menu.run()
        if action == "PLAY":
            self.state = GameState.PLAYING
        elif action == "HIGHSCORES":
            self.state = GameState.HIGHSCORES
        else:
            self.state = GameState.QUIT

    def _handle_playing(self):
        # run game loop on self.screen
        # when game ends (death / win):
        # self.current_score = final_score
        # self.state = GameState.NAME_INPUT
        pass

    def _handle_name_input(self):
        # render prompt: "Enter your name:"
        # on Enter:
        # self.highscores.add_score(name, self.current_score)
        # self.highscores.save_to_file()
        # self.state = GameState.HIGHSCORES
        pass

    def _handle_highscores(self):
        # render highscore table using self.highscores.scores
        # On Esc or Button click -> self.state = GameState.MENU
        self.highscores.load_file()

        font_title = pg.font.Font(None, 48)
        font_entry = pg.font.Font(None, 36)
        font_footer = pg.font.Font(None, 24)

        viewing = True
        while viewing and self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    viewing = False
                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_ESCAPE, pg.K_RETURN, pg.K_SPACE):
                        self.state = GameState.MENU
                        viewing = False

            self.screen.fill((5, 0, 25))
            title_surf = font_title.render("HIGH SCORES", True, (255, 255, 0))
            self.screen.blit(title_surf, title_surf.get_rect(
                center=(self.width // 2, 80)))
            y_pos = 160
            if not self.highscores.scores:
                no_scores_surf = font_entry.render(
                    "No scores yet!", True, (200, 200, 200))
                self.screen.blit(no_scores_surf, no_scores_surf.get_rect(
                    center=(self.width // 2, y_pos)))
            else:
                for rank, entry in enumerate(
                        self.highscores.scores[:10], start=1):
                    name = entry.get("name", "Unknown")
                    score = entry.get("score", 0)
                    text = f"{rank:2d}. {name:<12} {score:>6}"
                    line_surf = font_entry.render(text, True, (255, 255, 255))
                    self.screen.blit(line_surf, line_surf.get_rect(
                        center=(self.width // 2, y_pos)))
                    y_pos += 45

            footer_surf = font_footer.render(
                "Press ESC or SPACE to return", True, (150, 150, 150))
            self.screen.blit(footer_surf, footer_surf.get_rect(
                center=(self.width // 2, self.height - 50)))

            pg.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    manager = GameManager()
    manager.run()
