import pygame as pg


class DrawMaze:
    def __init__(self, maze: list[list[int]]):
        self.maze = maze

    def window(self):
        pg.init()
        cell_size = 50
        whidth: int = len(self.maze[0])
        height: int = len(self.maze)
        screen = pg.display.set_mode((whidth * cell_size, height * cell_size))

        running = True

        while running:
            for event in pg.event.get():
                if event.type is pg.QUIT:
                    running = False
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                running = False

            screen.fill((5, 0, 25))
            x = 0
            y = 0
            for a in range(height):
                for b in range(whidth):
                    cell = self.maze[b][a]
                    x = b * cell_size
                    y = a * cell_size
                    if cell & 1:
                        pg.draw.line(screen, (100, 90, 175), (y, x), (y + 50, x), 6)
                        pg.draw.line(screen, (175, 170, 255), (y, x), (y + 50, x), 2)
                    if cell & 2:
                        pg.draw.line(screen, (100, 90, 175), (y + 50, x), (y + 50, x + 50), 6)
                        pg.draw.line(screen, (175, 170, 255), (y + 50, x), (y + 50, x + 50), 2)
                    if cell & 4:
                        pg.draw.line(screen, (100, 90, 175), (y, x + 50), (y + 50 , x + 50), 6)
                        pg.draw.line(screen, (175, 170, 255), (y, x + 50), (y + 50 , x + 50), 2)
                    if cell & 8:
                        pg.draw.line(screen, (100, 90, 175), (y, x), (y, x + 50), 6)
                        pg.draw.line(screen, (175, 170, 255), (y, x), (y, x + 50), 2)

            pg.display.flip()
    pg.quit()
