import os
import sys
from src.parser import ConfigParser
from src.maze_loader import MazeLoader, MazeLoaderError


def run() -> None:
    if len(sys.argv) != 2:
        print("Error: Wrong number of arguments.")
        print("Try again with: uv run python3 pac-man.py config.json.")
        sys.exit(1)
    elif ".json" not in os.path.basename(sys.argv[1]):
        print("Error: Config file must be a json file.")
        print("Try again with: uv run python3 pac-man.py config.json.")
        sys.exit(1)

    config_path = sys.argv[1]
    try:
        with open(config_path, "r"):
            parser = ConfigParser(config_path)
            config = parser.parse()
            # just for checking
            print(config.__dict__)
    except FileNotFoundError:
        print(f"Error: File '{config_path}' not found.")
        sys.exit(1)

    # just for testing
    try:
        level = config.levels[0]
        maze_data = MazeLoader.load(
            width=level.width,
            height=level.height,
            seed=config.seed,
        )
        print(f"\n\nmaze generated: {maze_data.width}x{maze_data.height}")
    except MazeLoaderError as e:
        print("MazeLoaderError:", e)
        sys.exit(1)


if __name__ == "__main__":
    run()
