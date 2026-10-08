import json
from typing import Any


class ConfigError(Exception):
    pass


class LevelsConfig:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height


class GameConfig:
    def __init__(
        self,
        highscore_filename: str = "highscores.json",
        seed: int = 42,
        lives: int = 3,
        level_max_time: int = 90,
        points_per_pacgum: int = 10,
        points_per_super_pacgum: int = 50,
        points_per_ghost: int = 200,
        levels: list[LevelsConfig] | None = None
    ):
        self.highscore_filename = highscore_filename,
        self.seed = seed,
        self.lives = lives,
        self.level_max_time = level_max_time,
        self.points_per_pacgum = points_per_pacgum,
        self.points_per_super_pacgum = points_per_super_pacgum,
        self.points_per_ghost = points_per_ghost,
        self.levels = list[LevelsConfig]


class ConfigParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def _strip_comments(self, to_strip: str) -> str:
        cleaned: list[str] = []
        for line in to_strip.splitlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            cleaned.append(line)
        cleaned = "\n".join(cleaned)
        return cleaned

    def parse(self) -> GameConfig:
        try:
            with open(self.filepath, "r") as file:
                no_comments = self._strip_comments(file.read())
                config_dict: dict[str, Any] = json.loads(no_comments)
                if not isinstance(config_dict, dict):
                    raise ConfigError
        except json.JSONDecodeError as e:
            print("Error parsing config file:", e)
            print("Using default game config.")
            return GameConfig()
        except ConfigError:
            print("ConfigError: Invalid format in config.json.")
            print("Using default game config.")
            return GameConfig()

        stored = GameConfig()
        stored.highscore_filename = config_dict.get(
            "highscore_filename", "highscores.json")

        return stored
