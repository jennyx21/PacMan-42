import pygame
import pygame_menu
import pygame_menu.events


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
        self.action = None

    def build_menu(self) -> None:
        self.menu.add.label(
            "PAC-MAN",
            font_color=(255, 255, 0),
            font_size=64,
            margin=(0, 40),
        )
        self.menu.add.button('Play', self.play_function)
        self.menu.add.button('Highscores', self.show_highscores)
        self.menu.add.button('Quit', self.quit_function)

    def play_function(self) -> None:
        self.action = "PLAY"
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
        self.menu.mainloop(self.surface)
        return self.action


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    menu = GameMenu(screen)
    gamestart = menu.run()
    if gamestart:
        print("Play game")
    pygame.quit()
