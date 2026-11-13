import pygame
import pygame_menu
from typing import Optional


class GameMenu:
    def __init__(
            self,
            surface: pygame.Surface
    ) -> None:
        self.surface = surface
        self.width, self.height = surface.get_size()

        menutheme = pygame_menu.Theme(
            background_color=(5, 0, 25),
            widget_font_color=(200, 200, 200),
            selection_color=(255, 255, 0),
            widget_font_size=36,
            widget_margin=(0, 25)
        )
        menutheme.title = False

        self.menu = pygame_menu.Menu(
            width=self.width,
            height=self.height,
            title="PAC-MAN",
            theme=menutheme
        )
        self.build_menu()
        self.action: Optional[str] = None

    def build_menu(self) -> None:
        self.menu.add.label(
            "PAC-MAN",
            font_color=(255, 255, 0),
            font_size=64,
            margin=(0, 40),
        )
        self.menu.add.button('Play', self.play_function)
        self.menu.add.button('Instructions', self.show_instructions)
        self.menu.add.button('Highscores', self.show_highscores)
        self.menu.add.button('Quit', self.quit_function)

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
        self.menu.enable()
        clock = pygame.time.Clock()

        while self.menu.is_enabled():
            events = pygame.event.get()
            mapped_events = []
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
