import pygame as pg
from pygame import Surface
from src.player_mechanics import Game
from src.pacman import PacMan
from src.pacgum import Pacgum
from src.ghosts import Blinky, Pinky, Inky, Clyde



class DrawMaze:
    def __init__(self, maze: list[list[int]],
                 pacgum: int,
                 superpacgum: int,
                 points_pg: int,
                 points_spg: int,
                 lives: int,
                 screen: Surface,
                 score: int,
                 level: int):
        self.maze = maze
        self.pacgum = pacgum
        self.superpacgum = superpacgum
        self.points_pacgum = points_pg
        self.points_super_pacgum = points_spg
        self.lives = lives
        self.screen = screen
        self.score = score
        self.level = level

    def window(self):
        pg.init()
        clock = pg.time.Clock()
        whidth: int = 700
        height: int = 700
        cell_size = whidth / len(self.maze)
        middle = len(self.maze) / 2
        background = pg.Surface((whidth + 2 * 50, height + 2 * 50))
        field = pg.Surface((whidth, height))
        game = Game(background, self.score, self.lives, self.level)
        pacman = PacMan(field,
                        game,
                        self.maze,
                        cell_size,
                        (int(middle), int(middle)),
                        self.lives)
        pacgum = Pacgum(field,
                        self.pacgum,
                        self.superpacgum,
                        self.points_pacgum,
                        self.points_super_pacgum,
                        self.maze,
                        cell_size,
                        pacman,
                        game)
        blinky = Blinky(field, cell_size, self.maze, pacman, game)
        pinky = Pinky(field, cell_size, self.maze, pacman, game)
        inky = Inky(field, cell_size, self.maze, pacman, game)
        clyde = Clyde(field, cell_size, self.maze, pacman, game)
        running = True

        while running:
            events = pg.event.get()
            for event in events:
                if event.type is pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key is pg.K_c:
                        game.turn_on_cheat()

            start, pause = game.game_info()
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                running = False
            if keys[pg.K_SPACE] or keys[pg.K_KP_ENTER]:
                if start is not True:
                    game.update_start()
                elif start is True:
                    game.update_start()

            background.fill((15, 10, 40))
            field.fill((15, 10, 40))
            self.draw_walls(cell_size, field, (100, 90, 175), 8, 3)
            self.draw_walls(cell_size, field, (175, 170, 255), 3)

            pacman.draw_pacman(int(middle * cell_size),
                               int(middle * cell_size))
            pacgum.run_gums()
            blinky.run_blinky()
            game.display_highscore()
            game.diplay_lives()
            game.display_Level()
            if game.lives_info() == 0:
                running = False

            # pinky.run_pinky()
            # inky.run_inky()
            # clyde.run_clyde()
            self.screen.blit(background, background.get_rect())
            self.screen.blit(field,
                             field.get_rect(center=self.screen.
                                            get_rect().center))
            pg.display.flip()
            clock.tick(60)

    def draw_walls(self,
                   cell_size: float,
                   screen: Surface,
                   color: tuple[int, int, int],
                   size: int,
                   length: int = 0):
        x: float = 0
        y: float = 0
        i: int = 0
        for a in range(len(self.maze)):
            for b in range(len(self.maze[i])):
                cell = self.maze[b][a]
                x = b * cell_size
                y = a * cell_size
                if cell & 1:
                    pg.draw.line(screen, color, (y - length, x),
                                 (y + cell_size + length, x), size)
                if cell & 2:
                    pg.draw.line(screen, color,
                                 (y + cell_size, x - length),
                                 (y + cell_size, x + cell_size + length), size)
                if cell & 4:
                    pg.draw.line(screen, color,
                                 (y, x + cell_size),
                                 (y + cell_size, x + cell_size), size)
                if cell & 8:
                    pg.draw.line(screen, color,
                                 (y, x), (y, x + cell_size), size)
            i += 1
        return
