import json
from typing import Any


class HighscoreRecord:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.scores: list[dict[str, Any]] = []

    def load_file(self) -> None:
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                self.scores = []
                return
        except Exception:
            print("Failed to load the leaderboard :(")

    def add_score(self, name: str, score: int) -> None:
        max_scores = 10
        self.scores.append({"name": name, "score": score})
        self.scores.sort(key=lambda x: x.get("score", 0), reverse=True)
        self.scores = self.scores[:max_scores]

    def save_to_file(self) -> None:
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.scores, f)
            print("Your score is saved :)")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    hs = HighscoreRecord("highscores.json")
    hs.load_file()
    print()

    hs.add_score("weng", 20)
    hs.save_to_file()
    print("self.scores:", hs.scores)
    print()

    hs.add_score("w", 50.6)
    hs.save_to_file()
    print(hs.scores)
    print()

    hs.add_score("oooooooooooo", 10)
    hs.save_to_file()
    print(hs.scores)
    print()
