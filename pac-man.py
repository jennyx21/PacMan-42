import os
import sys
from src.parser import ConfigParser
from src.game_manager import GameManager
from src.asset_helper import resource_path


def run() -> None:
    if len(sys.argv) == 1:
        config_path = str(resource_path("config.json"))
    elif len(sys.argv) == 2:
        config_path = sys.argv[1]
        if ".json" not in os.path.basename(config_path):
            print("Error: Config file must be a json file.")
            sys.exit(1)
    else:
        print("Error: Wrong number of arguments.")
        print("Try again with: uv run python3 pac-man.py config.json.")
        sys.exit(1)
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
