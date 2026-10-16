import json
from typing import Any


class HighscoreRecord:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.scores: list[dict[str, Any]] = []
        self.load_file()

    def load_file(self) -> None:
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                self.scores = []
                return
        except Exception:
            print("Failed to load the leaderboard :(")
