from dataclasses import dataclass


class MazeLoaderError(Exception):
    pass


@dataclass
class MazeData:
    grid: list[list[int]]
    width: int
    height: int


class MazeLoader:
    @staticmethod
    def load(width: int, height: int, seed: int = 0) -> MazeData:
        try:
            # type: ignore[import-untyped]
            from mazegenerator.mazegenerator import MazeGenerator
        except ImportError as e:
            print(f"MazeLoader error: {e}. Using fallback maze.")
            return MazeLoader._fallback_maze(width, height, seed=seed)

        try:
            generator = MazeGenerator(
                size=(width, height),
                entry_cell=(0, 0),
                exit_cell=(0, 0),
                perfect=False,
                seed=seed,
            )
            raw_grid = generator.maze
        except Exception as e:
            print(f"MazeLoader error: {e}. Using fallback maze.")
            return MazeLoader._fallback_maze(width, height, seed=seed)

        if (not isinstance(raw_grid, list)
                or not raw_grid
                or not isinstance(raw_grid[0], list)):
            print("MazeLoader error: Invalid grid. Using fallback maze.")
            return MazeLoader._fallback_maze(width, height, seed=seed)

        return MazeData(
            grid=raw_grid,
            width=len(raw_grid[0]),
            height=len(raw_grid),
        )

    @staticmethod
    def _fallback_maze(width: int, height: int, seed: int = 42) -> MazeData:
        import random
        rng = random.Random(seed)

        # 1. Start with every cell having all 4 walls (15)
        grid = []
        for _ in range(height):
            grid.append([15] * width)

        visited = []
        for _ in range(height):
            visited.append([False] * width)

        # directions: (d_row, d_col, wall_current, wall_neighbor)
        dirs = [
            (-1, 0, 1, 4),  # UP
            (1, 0, 4, 1),   # DOWN
            (0, 1, 2, 8),   # RIGHT
            (0, -1, 8, 2),  # LEFT
        ]

        start_r, start_c = height // 2, width // 2
        visited[start_r][start_c] = True

        # from_r, from_c, to_r, to_c, wall_curr, wall_next
        walls = []
        for dr, dc, w_curr, w_next in dirs:
            nr, nc = start_r + dr, start_c + dc
            if 0 <= nr < height and 0 <= nc < width:
                walls.append((start_r, start_c, nr, nc, w_curr, w_next))

        while walls:
            # pick random wall
            idx = rng.randrange(len(walls))
            r, c, nr, nc, w_curr, w_next = walls.pop(idx)

            if not visited[nr][nc]:
                # knock down the wall between (r, c) and (nr, nc)
                grid[r][c] -= w_curr
                grid[nr][nc] -= w_next
                visited[nr][nc] = True

                # new unvisited neighbors
                for dr, dc, nw_curr, nw_next in dirs:
                    nnr, nnc = nr + dr, nc + dc
                    if 0 <= nnr < height and 0 <= nnc < width and not visited[nnr][nnc]:
                        walls.append((nr, nc, nnr, nnc, nw_curr, nw_next))

        # remove 20% of the remaining walls
        for r in range(1, height - 1):
            for c in range(1, width - 1):
                if rng.random() < 0.20:
                    dr, dc, w_curr, w_next = rng.choice(dirs)
                    nr, nc = r + dr, c + dc
                    if 0 < nr < height - 1 and 0 < nc < width - 1:
                        if grid[r][c] & w_curr:
                            grid[r][c] -= w_curr
                            grid[nr][nc] -= w_next

        # clear pac man spawn area
        for r in range(start_r - 1, start_r + 2):
            for c in range(start_c - 1, start_c + 2):
                if 0 <= r < height and 0 <= c < width:
                    if r > start_r - 1 and (grid[r][c] & 1):
                        grid[r][c] -= 1
                        grid[r - 1][c] -= 4
                    if c > start_c - 1 and (grid[r][c] & 8):
                        grid[r][c] -= 8
                        grid[r][c - 1] -= 2

        return MazeData(grid=grid, width=width, height=height)


if __name__ == '__main__':
    from src.drawmaze import DrawMaze

    data = MazeLoader._fallback_maze(12, 12)
    visualizer = DrawMaze(
        maze=data.grid,
        pacgum=42,
        superpacgum=4,
        points_pg=10,
        points_spg=50,
        points_ghost=200,
        lives=3,
        max_time=90
    )
    visualizer.window()
# uv run python3 -m src.maze_loader
