import json


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

    def strip_comments(self) -> None:
        pass
    
    def parse(self) -> GameConfig:
        pass