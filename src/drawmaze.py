from dataclasses import dataclass
import pygame as pg
from pygame import Surface
from src.player_mechanics import Game
from src.pacman import PacMan
from src.pacgum import Pacgum
from src.ghosts import Blinky, Pinky, Inky, Clyde


@dataclass
class Results():
    outcome: str
    score: int
    lives: int


class DrawMaze:
    def __init__(self, maze: list[list[int]],
                 pacgum: int,
                 superpacgum: int,
                 points_pg: int,
                 points_spg: int,
                 points_ghost: int,
                 lives: int,
                 max_time: int = 90,
                 screen: Surface | None = None,
                 score: int = 0,
                 level: int = 1):
        self.maze = maze
        self.pacgum = pacgum
        self.superpacgum = superpacgum
        self.points_pacgum = points_pg
        self.points_super_pacgum = points_spg
        self.points_ghost = points_ghost
        self.lives = lives
        self.screen = screen
        self.score = score
        self.level = level
        self.max_time = max_time

    def window(self, screen: Surface | None = None, clock: pg.time.Clock | None = None) -> Results:
        standalone = screen is None
        if standalone:
            pg.init()
            clock = pg.time.Clock()
            whidth: int = 700
            height: int = 700
            self.screen = pg.display.set_mode(
                (whidth + 2 * 50, height + 2 * 50))
            pg.display.set_caption("Pac Man")
        elif screen is not None:
            self.screen = screen

        if clock is None:
            clock = pg.time.Clock()

        whidth: int = 700
        height: int = 700
        cell_size = whidth / len(self.maze)
        middle = len(self.maze) / 2
        background = pg.Surface((whidth + 2 * 50, height + 2 * 50))
        field = pg.Surface((whidth, height))
        game = Game(background, self.score, self.lives, self.level,
                    self.max_time)
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

        font_pause = pg.font.Font(None, 64)
        font_sub = pg.font.Font(None, 28)
        running = True
        outcome = "QUIT"

        while running:
            events = pg.event.get()
            for event in events:
                if event.type is pg.QUIT:
                    outcome = "QUIT"
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key is pg.K_c:
                        game.turn_on_cheat()
                    elif event.key == pg.K_ESCAPE:
                        outcome = "BACK"
                        running = False
                    elif event.key == pg.K_SPACE:
                        game.update_start()

            start, pause = game.game_info()

            background.fill((15, 10, 40))
            field.fill((15, 10, 40))
            self.draw_walls(cell_size, field, (100, 90, 175), 8, 3)
            self.draw_walls(cell_size, field, (175, 170, 255), 3)

            pacman.draw_pacman(int(middle * cell_size),
                               int(middle * cell_size))
            pacgum.run_gums()
            blinky.run_blinky()
            pinky.run_pinky()
            inky.run_inky()
            clyde.run_clyde()
            game.display_highscore()
            game.diplay_lives()
            game.display_Level()
            if game.start:
                game.display_time()

            if game.level_lost:
                outcome = "LOSE"
                running = False

            if game.level_win:
                outcome = "WIN"
                running = False

            self.screen.blit(background, background.get_rect())
            self.screen.blit(field,
                             field.get_rect(center=self.screen.
                                            get_rect().center))

            # dim screen before start, pause and game over
            if not start:
                overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                self.screen.blit(overlay, (0, 0))

                banner_surf = font_sub.render(
                    "PRESS SPACE TO START", True, (255, 255, 0))
                self.screen.blit(
                    banner_surf,
                    banner_surf.get_rect(center=(self.screen.get_width() // 2,
                                                 self.screen.get_height() // 2)))
            elif pause:
                overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                self.screen.blit(overlay, (0, 0))

                pause_surf = font_pause.render("PAUSED", True, (255, 255, 0))
                self.screen.blit(
                    pause_surf,
                    pause_surf.get_rect(center=(self.screen.get_width() // 2,
                                                 self.screen.get_height() // 2 - 25)))

                resume_surf = font_sub.render(
                    "PRESS SPACE TO RESUME", True, (200, 200, 200))
                self.screen.blit(
                    resume_surf,
                    resume_surf.get_rect(center=(self.screen.get_width() // 2,
                                                 self.screen.get_height() // 2 + 25)))
                resume_surf = font_sub.render(
                    " OR ESC TO EXIT", True, (200, 200, 200))
                self.screen.blit(
                    resume_surf,
                    resume_surf.get_rect(center=(self.screen.get_width() // 2,
                                                 self.screen.get_height() // 2 + 65)))

            pg.display.flip()
            clock.tick(60)

        if outcome in ("LOSE", "WIN"):
            overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            title = "GAME OVER" if outcome == "LOSE" else "YOU WIN!"
            color = (255, 60, 60) if outcome == "LOSE" else (60, 255, 60)
            over_surf = font_pause.render(title, True, color)
            self.screen.blit(
                over_surf,
                over_surf.get_rect(center=(self.screen.get_width() // 2,
                                           self.screen.get_height() // 2 - 30)))

            score_surf = font_sub.render(
                f"FINAL SCORE: {game.highscore}", True, (255, 255, 0))
            self.screen.blit(
                score_surf,
                score_surf.get_rect(center=(self.screen.get_width() // 2,
                                            self.screen.get_height() // 2 + 20)))

            prompt_surf = font_sub.render(
                "PRESS ANY KEY TO CONTINUE...", True, (200, 200, 200))
            self.screen.blit(
                prompt_surf,
                prompt_surf.get_rect(center=(self.screen.get_width() // 2,
                                             self.screen.get_height() // 2 + 65)))

            pg.display.flip()

            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        outcome = "QUIT"
                        waiting = False
                    elif event.type == pg.KEYDOWN:
                        waiting = False
                clock.tick(60)

        if standalone:
            pg.quit()

        return Results(outcome, game.highscore, game.pacman_lives)

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
