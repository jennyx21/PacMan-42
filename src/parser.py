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
    pacgum: int = 42
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
        return "\n".join(cleaned)

    def _get_value(
            self, data: dict[str, Any], key: str, expected_type: type) -> Any:
        if key not in data:
            raise ConfigError(f"Invalid key for '{key}' in config.json")
        val = data[key]
        if not isinstance(val, expected_type):
            raise ConfigError(f"Invalid type for '{key}' in config.json")
        return val

    def _parse_levels(self, config_lvl: object) -> list[LevelsConfig]:
        if not isinstance(config_lvl, list):
            raise ConfigError("'levels' must be a list")

        levels_list: list[LevelsConfig] = []
        max_cells = 25

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

            if width > max_cells:
                raise ConfigError(f"'{max_cells}' is the maximum width "
                                  "we take to fit the window.")
            elif height > max_cells:
                raise ConfigError(f"'{max_cells}' is the maximum width "
                                  "we take to fit the window.")

            if width != height:
                print(
                    "Oops! Sorry, Jenny and Weng don't like a game window that"
                    " is not a square :(")
                if width > height:
                    height = width
                else:
                    width = height
                print("So we force it into a square anyway (^o^)/\\(^o^)")

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
        try:
            stored.highscore_filename = self._get_value(
                config_dict, "highscore_filename", str)
            stored.seed = self._get_value(config_dict, "seed", int)
            stored.lives = self._get_value(config_dict, "lives", int)
            stored.level_max_time = self._get_value(
                config_dict, "level_max_time", int)
            stored.pacgum = self._get_value(config_dict, "pacgum", int)
            stored.points_per_pacgum = self._get_value(
                config_dict, "points_per_pacgum", int)
            stored.points_per_super_pacgum = self._get_value(
                config_dict, "points_per_super_pacgum", int)
            stored.points_per_ghost = self._get_value(
                config_dict, "points_per_ghost", int)

            if "levels" not in config_dict:
                raise ConfigError("Invalid key for 'levels' in config.json")
            stored.levels = self._parse_levels(config_dict["levels"])

        except ConfigError as e:
            print("ConfigError:", e)
            print("Using default game config for invalid and/or missing keys.")

        return stored
