import pygame
import pygame_menu
from src.asset_helper import asset_loader
from src.highscores import HighscoreRecord
from typing import Optional


class GameMenu:
    def __init__(
            self,
            surface: pygame.Surface,
            highscores: Optional[HighscoreRecord] = None
    ) -> None:
        self.surface = surface
        self.menue_backround = asset_loader("Menu", "start", 20)
        self.current: float = 0
        self.highscores = highscores
        self.width, self.height = surface.get_size()

        menutheme = pygame_menu.Theme(
            background_color=(0, 0, 0, 0),
            widget_font_color=(200, 200, 200),
            selection_color=(255, 255, 0),
            widget_font=pygame_menu.font.FONT_MUNRO,
            widget_font_size=44,
            widget_margin=(0, 8),
            widget_offset=(0, 100)
        )
        menutheme.title = False

        self.menu = pygame_menu.Menu(
            width=self.width,
            height=self.height,
            title="PAC-MAN",
            theme=menutheme,
            center_content=False
        )
        self.build_menu()
        self.action: Optional[str] = None

    def build_menu(self) -> None:
        self.menu.clear()
        self.menu.add.label(
            " PAC MAN",
            font_name=pygame_menu.font.FONT_8BIT,
            font_size=88,
            margin=(0, 20),
        )
        self.menu.add.label("", font_size=10, margin=(0, 10))

        self.menu.add.button('Play', self.play_function)
        self.menu.add.button('Instructions', self.show_instructions)
        self.menu.add.button('Highscores', self.show_highscores)
        self.menu.add.button('Quit', self.quit_function)
        self.menu.add.label("", font_size=1, margin=(0, 10))
        self.menu.add.label(
            "--- BEST RECORDS ---",
            font_color=(255, 255, 0),
            font_size=22,
            margin=(0, 5),
        )

        if self.highscores:
            self.highscores.load_file()
            top3 = self.highscores.scores[:3]
            if not top3:
                self.menu.add.label(
                    "No scores yet!",
                    font_color=(150, 150, 150),
                    font_size=16,
                    margin=(0, 2),
                )
            else:
                for rank, entry in enumerate(top3, start=1):
                    name = entry.get("name", "Player")
                    score = entry.get("score", 0)
                    self.menu.add.label(
                        f"{rank}. {name:<12}{score:>6}",
                        font_color=(220, 220, 220),
                        font_size=18,
                        margin=(0, 2),
                    )
                self.menu.add.label(
                    "(see more in highscores...)",
                    font_size=16,
                    margin=(0, 5),
                )

    def play_function(self) -> None:
        self.action = "PLAY"
        self.menu.disable()

    def show_instructions(self) -> None:
        self.action = "INSTRUCTIONS"
        self.menu.disable()

    def show_highscores(self) -> None:
        self.action = "HIGHSCORES"
        self.menu.disable()

    def quit_function(self) -> None:
        self.action = "QUIT"
        self.menu.disable()

    def run(self) -> str:
        self.action = "QUIT"
        self.build_menu()
        self.menu.enable()
        clock = pygame.time.Clock()

        while self.menu.is_enabled():
            events = pygame.event.get()
            mapped_events = []
            if self.current < len(self.menue_backround):
                image = self.menue_backround[int(self.current)]
                rect = image.get_rect()
                self.current += 0.2
            else:
                self.current = 0
                image = self.menue_backround[int(self.current)]
                rect = image.get_rect()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        mapped_events.append(
                            pygame.event.Event(pygame.KEYDOWN,
                                               key=pygame.K_UP))
                    elif event.key == pygame.K_s:
                        mapped_events.append(
                            pygame.event.Event(pygame.KEYDOWN,
                                               key=pygame.K_DOWN))
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        mapped_events.append(
                            pygame.event.Event(pygame.KEYDOWN,
                                               key=pygame.K_LEFT))
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        mapped_events.append(
                            pygame.event.Event(pygame.KEYDOWN,
                                               key=pygame.K_RIGHT))
                    elif event.key == pygame.K_SPACE:
                        mapped_events.append(
                            pygame.event.Event(pygame.KEYDOWN,
                                               key=pygame.K_RETURN))
                    else:
                        mapped_events.append(event)
                else:
                    mapped_events.append(event)

            self.menu.update(mapped_events)
            if self.menu.is_enabled():
                self.surface.blit(image, rect)
                self.menu.draw(self.surface)
            pygame.display.flip()
            clock.tick(60)

        return self.action


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    menu = GameMenu(screen)
    gamestart = menu.run()
    if gamestart:
        print("Play game")
    pygame.quit()
