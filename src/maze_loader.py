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
    def _fallback_maze(width: int, height: int, seed: int = 42) -> MazeData:
        import random
        rng = random.Random(seed)

        # 1. Start with all walls closed (15 = 1 | 2 | 4 | 8) for every cell
        grid = [[15 for _ in range(width)] for _ in range(height)]
        visited = [[False for _ in range(width)] for _ in range(height)]

        # Directions: (d_row, d_col, current_wall_bit, opposite_wall_bit)
        # UP: 1, RIGHT: 2, DOWN: 4, LEFT: 8
        dirs = [
            (-1, 0, 1, 4),  # UP
            (0, 1, 2, 8),   # RIGHT
            (1, 0, 4, 1),   # DOWN
            (0, -1, 8, 2),  # LEFT
        ]

        # 2. Carve corridors using DFS
        def dfs(r: int, c: int) -> None:
            visited[r][c] = True
            shuffled_dirs = dirs[:]
            rng.shuffle(shuffled_dirs)

            for dr, dc, wall, opp in shuffled_dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width and not visited[nr][nc]:
                    # Knock down the wall between (r, c) and (nr, nc)
                    grid[r][c] &= ~wall
                    grid[nr][nc] &= ~opp
                    dfs(nr, nc)

        # Start carving from (1, 1)
        dfs(1, 1)

        # 3. Add loops (Pac-Man needs loops so you don't get trapped by ghosts)
        for r in range(1, height - 1):
            for c in range(1, width - 1):
                if rng.random() < 0.20:
                    dr, dc, wall, opp = rng.choice(dirs)
                    nr, nc = r + dr, c + dc
                    if 0 < nr < height - 1 and 0 < nc < width - 1:
                        grid[r][c] &= ~wall
                        grid[nr][nc] &= ~opp

        # 4. Clear the center 3x3 spawn area for Pac-Man
        mid_r, mid_c = height // 2, width // 2
        for r in range(mid_r - 1, mid_r + 2):
            for c in range(mid_c - 1, mid_c + 2):
                if 0 <= r < height and 0 <= c < width:
                    if r > mid_r - 1:
                        grid[r][c] &= ~1
                        grid[r - 1][c] &= ~4
                    if r < mid_r + 1:
                        grid[r][c] &= ~4
                        grid[r + 1][c] &= ~1
                    if c > mid_c - 1:
                        grid[r][c] &= ~8
                        grid[r][c - 1] &= ~2
                    if c < mid_c + 1:
                        grid[r][c] &= ~2
                        grid[r][c + 1] &= ~8

        return MazeData(grid=grid, width=width, height=height)

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
            print(f"MazeLoader error: {e}. Using fallback maze.")
            return MazeLoader._fallback_maze(width, height, seed=seed)

        return MazeData(
            grid=raw_grid,
            width=len(raw_grid[0]),
            height=len(raw_grid),
        )
