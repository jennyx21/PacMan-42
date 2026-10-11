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
            raise MazeLoaderError(
                f"MazeLoaderError: {e}.\nEnsure the wheel is installed with"
                "'uv pip install <wheel_file>'."
            )

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
            raise MazeLoaderError(
                f"MazeLoaderError: External MazeGenerator crashed, {e}"
            )

        if (not isinstance(raw_grid, list)
                or not raw_grid
                or not isinstance(raw_grid[0], list)):
            raise MazeLoaderError(
                "MazeLoaderError: External MazeGenerator returned "
                "an invalid grid structure."
            )

        return MazeData(
            grid=raw_grid,
            width=len(raw_grid[0]),
            height=len(raw_grid),
        )
