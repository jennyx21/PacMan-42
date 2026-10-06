import sys
import json
from src.parser import parse_config


def run() -> None:
    if len(sys.argv) != 2:
        print("Try again with: uv run python3 pac-man.py config.json.")

    config_path = "config.json"
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            print(config)
    except FileNotFoundError:
        print(f"File '{config_path}' not found.")


if __name__ == "__main__":
    run()
