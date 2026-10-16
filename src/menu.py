import pygame
import pygame_menu
import pygame_menu.events


class GameMenu:
    def __init__(self, surface: pygame.Surface, title: str):
        self.surface = surface
        self.width = surface.get_size()
        self.height = self.width
        self.menu = pygame_menu.Menu(
            title='Pac-Man',
            width=self.width,
            height=self.height
        )
        self.build_menu
        self.start_game = False

    def build_menu(self) -> None:
        self.menu.add.button('Play', self.play_function)
        self.menu.add.button('Highscores', self.show_highscores)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def play_function(self) -> bool:
        self.menu.disable()
        self.menu.mainloop(self.surface)
        self.start_game = True
        return self.start_game

    def show_highscores(self) -> None:
        print("Highscores")



