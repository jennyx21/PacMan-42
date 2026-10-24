import pygame as pg
from src.player_mechanics import Game
from src.pacman import PacMan


class DrawMaze:
    def __init__(self, maze: list[list[int]]):
        self.maze = maze

    def window(self):
        pg.init()
        clock = pg.time.Clock()
        whidth: int = 800
        height: int = 800
        cell_size = whidth / len(self.maze)
        screen = pg.display.set_mode((whidth, height))
        pg.display.set_caption("Pac Man")
        game = Game()
        pacman = PacMan(screen, game)
        running = True

        while running:
            for event in pg.event.get():
                if event.type is pg.QUIT:
                    running = False

            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                running = False
            if keys[pg.K_SPACE] or keys[pg.K_KP_ENTER]:
                game.update_start()

            screen.fill((5, 0, 25))
            x = 0
            y = 0
            i = 0
            for a in range(len(self.maze)):
                for b in range(len(self.maze[i])):
                    cell = self.maze[b][a]
                    x = b * cell_size
                    y = a * cell_size
                    if cell & 1:
                        pg.draw.line(screen, (100, 90, 175), (y - 3, x),
                                     (y + cell_size + 3, x), 8)
                    if cell & 2:
                        pg.draw.line(screen, (100, 90, 175),
                                     (y + cell_size, x - 3),
                                     (y + cell_size, x + cell_size + 3), 8)
                    if cell & 4:
                        pg.draw.line(screen, (100, 90, 175),
                                     (y, x + cell_size),
                                     (y + cell_size, x + cell_size), 8)
                    if cell & 8:
                        pg.draw.line(screen, (100, 90, 175),
                                     (y, x), (y, x + cell_size), 8)
                i += 1

            x = 0
            y = 0
            i = 0
            for a in range(len(self.maze)):
                for b in range(len(self.maze[i])):
                    cell = self.maze[b][a]
                    x = b * cell_size
                    y = a * cell_size
                    if cell & 1:
                        pg.draw.line(screen, (175, 170, 255), (y, x),
                                     (y + cell_size, x), 2)
                    if cell & 2:
                        pg.draw.line(screen, (175, 170, 255),
                                     (y + cell_size, x),
                                     (y + cell_size, x + cell_size), 2)
                    if cell & 4:
                        pg.draw.line(screen, (175, 170, 255),
                                     (y, x + cell_size),
                                     (y + cell_size, x + cell_size), 2)
                    if cell & 8:
                        pg.draw.line(screen, (175, 170, 255),
                                     (y, x), (y, x + cell_size), 2)
                i += 1
            pacman.draw_pacman(int(((len(self.maze) // 2) * cell_size) +
                               cell_size / 6),
                               int(((len(self.maze) // 2) * cell_size)) +
                               cell_size / 6)

            pg.display.flip()
            clock.tick(60)
    pg.quit()

    def walls()