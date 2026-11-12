import os
import sys
from src.parser import ConfigParser
from src.game_manager import GameManager


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
    except FileNotFoundError:
        print(f"Error: File '{config_path}' not found.")
        sys.exit(1)

    game = GameManager(config)
    game.run()


if __name__ == "__main__":
    run()
