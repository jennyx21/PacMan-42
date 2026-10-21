import json
from typing import Any


class HighscoreRecord:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.scores: list[dict[str, Any]] = []
        self.load_file()

    def _name_is_valid(self, name: str) -> bool:
        if not name or len(name) > 10:
            return False
        for char in name:
            if char.isalnum() or char == " ":
                continue
            else:
                return False
        return True

    def _score_is_valid(self, score: int) -> bool:
        if not isinstance(score, int):
            return False
        elif score < 0:
            return False
        return True

    def load_file(self) -> None:
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                self.scores = []
                return
            else:
                valid_pair: list[dict[str, Any]] = []
                for pair in data:
                    if not isinstance(pair, dict):
                        continue
                    n = pair.get("name", "")
                    s = pair.get("score", -1)
                    if self._name_is_valid(n) and self._score_is_valid(s):
                        valid_pair.append({"name": n, "score": s})

                self.scores = valid_pair

        except (FileNotFoundError, json.JSONDecodeError):
            self.scores = []
        except Exception as e:
            print(e)
            print("Failed to load the leaderboard :(")

    def add_score(self, name: str, score: int) -> None:
        max_scores = 10
        if not self._name_is_valid(name):
            print("Name cannot be empty or longer than 10 characters :(")
            return
        if not self._score_is_valid(score):
            print("Score can only be positive integers :(")
            return
        self.scores.append({"name": name, "score": score})
        self.scores.sort(key=lambda x: x.get("score", 0), reverse=True)
        self.scores = self.scores[:max_scores]
        print("Your score is saved :)")

    def save_to_file(self) -> None:
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.scores, f, indent=4)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    hs = HighscoreRecord("highscores.json")
    hs.load_file()
    print()

    hs.add_score("weng", 20)
    hs.add_score("", 200)
    hs.add_score("w", 50.6)  # type: ignore
    hs.add_score("oooooooooooo", 10)
    hs.save_to_file()
    print("leaderboard:", hs.scores)
    print()
