import json
from typing import Any
from dataclasses import dataclass, field


class ConfigError(Exception):
    pass


@dataclass
class LevelsConfig:
    level_id: int = 1
    width: int = 20
    height: int = 20


@dataclass
class GameConfig:
    highscore_filename: str = "highscores.json"
    seed: int = 42
    lives: int = 3
    level_max_time: int = 90
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    levels: list[LevelsConfig] = field(
        default_factory=lambda: [LevelsConfig()])


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
        stripped = "\n".join(cleaned)
        return stripped

    def _parse_levels(self, config_lvl: object) -> list[LevelsConfig]:
        if not isinstance(config_lvl, list):
            raise ConfigError("'levels' must be a list")

        levels_list: list[LevelsConfig] = []
        for lvl in config_lvl:
            if not isinstance(lvl, dict):
                raise ConfigError("Each level must be an object")
            try:
                level_id = lvl["level"]
                width = lvl["width"]
                height = lvl["height"]
            except KeyError as e:
                raise ConfigError(f"key {e} is not found in config file")

            if not isinstance(level_id, int):
                raise ConfigError("'level' must be an integer")
            if not isinstance(width, int) or width <= 0:
                raise ConfigError("'width' must be a positive integer")
            if not isinstance(height, int) or height <= 0:
                raise ConfigError("'height' must be a positive integer")

            levels_list.append(LevelsConfig(
                level_id=level_id, width=width, height=height))
        return levels_list

    def parse(self) -> GameConfig:
        try:
            with open(self.filepath, "r") as file:
                no_comments = self._strip_comments(file.read())
                config_dict: dict[str, Any] = json.loads(no_comments)
                if not isinstance(config_dict, dict):
                    raise ConfigError
        except json.JSONDecodeError as e:
            print("Error parsing config file:", e)
            print("Using default game config...")
            return GameConfig()
        except ConfigError:
            print("ConfigError: Invalid format in config.json")
            print("Using default game config.")
            return GameConfig()

        stored = GameConfig()
        stored.highscore_filename = config_dict.get(
            "highscore_filename", "highscores.json")
        stored.seed = config_dict.get("seed", 42)
        stored.lives = config_dict.get("lives", 3)
        stored.level_max_time = config_dict.get("level_max_time", 90)
        stored.points_per_pacgum = config_dict.get("points_per_pacgum", 10)
        stored.points_per_super_pacgum = config_dict.get(
            "points_per_super_pacgum", 50)
        stored.points_per_ghost = config_dict.get("points_per_ghost", 200)
        stored.levels = self._parse_levels(config_dict.get("levels", []))

        return stored
