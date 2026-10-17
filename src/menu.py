import pygame
import pygame_menu
import pygame_menu.events


class GameMenu:
    def __init__(self, surface: pygame.Surface, title: str = "Pac-Man") -> None:
        self.surface = surface
        self.width, self.height = surface.get_size()
        self.menu = pygame_menu.Menu(
            title=title,
            width=self.width,
            height=self.height
        )
        self.build_menu()
        self.start_game = False

    def build_menu(self) -> None:
        self.menu.add.button('Play', self.play_function)
        self.menu.add.button('Highscores', self.show_highscores)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def play_function(self) -> bool:
        self.menu.disable()
        self.start_game = True
        return self.start_game

    def show_highscores(self) -> None:
        print("Highscores")

    def run(self) -> bool:
        self.menu.enable()
        self.menu.mainloop(self.surface)
        return self.start_game


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    menu = GameMenu(screen)
    gamestart = menu.run()
    if gamestart:
        print("Play game")
    pygame.quit()
