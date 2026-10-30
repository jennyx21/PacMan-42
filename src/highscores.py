import json
from typing import Any
import pygame as pg


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
        if isinstance(score, bool) or not isinstance(score, int):
            return False
        return score >= 0

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


class Leaderboard:
    def __init__(self, record: HighscoreRecord) -> None:
        self.record = record
        self.font_title = pg.font.Font(None, 48)
        self.font_entry = pg.font.Font(None, 36)
        self.font_footer = pg.font.Font(None, 24)

    def display(self, screen: pg.Surface, clock: pg.time.Clock) -> str:
        self.record.load_file()
        width, height = screen.get_size()

        screen.fill((5, 0, 25))
        title_surf = self.font_title.render(
            "HIGH SCORES", True, (255, 255, 0))
        screen.blit(title_surf, title_surf.get_rect(
            center=(width // 2, 80)))

        y_pos = 160
        if not self.record.scores:
            no_scores = self.font_entry.render(
                "No scores yet!", True, (200, 200, 200))
            screen.blit(no_scores, no_scores.get_rect(
                center=(width // 2, y_pos)))
        else:
            for rank, entry in enumerate(self.record.scores[:10], start=1):
                name = entry.get("name", "Unknown")
                score = entry.get("score", 0)
                text = f"{rank:2d}. {name:<12} {score:>6}"
                surf = self.font_entry.render(
                    text, True, (255, 255, 255))
                screen.blit(surf, surf.get_rect(
                    center=(width // 2, y_pos)))
                y_pos += 45

        footer = self.font_footer.render(
            "Press ESC or SPACE to return", True, (150, 150, 150))
        screen.blit(footer, footer.get_rect(
            center=(width // 2, height - 50)))

        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "QUIT"
                elif event.type == pg.KEYDOWN and event.key in (pg.K_ESCAPE, pg.K_RETURN, pg.K_SPACE):
                    return "BACK"

            clock.tick(60)


class NameInput:
    def __init__(self, record: HighscoreRecord) -> None:
        self.record = record
        self.font_title = pg.font.Font(None, 48)
        self.font_entry = pg.font.Font(None, 36)
        self.font_footer = pg.font.Font(None, 24)

    def get_name(self) -> str:
        width, height = screen.get_size()
        input = True

        while input


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
