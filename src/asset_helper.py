from pathlib import Path
import sys
from pygame import Surface
import pygame
import re


def resource_path(relative: str) -> Path:
    """Path that works both normally and inside a PyInstaller build."""
    base = getattr(sys, "_MEIPASS", None)
    if base is not None:
        return Path(base) / relative
    return Path(__file__).resolve().parent.parent / relative


def frame_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    return int(match.group(1)) if match else 0


def asset_loader(name: str, direction: str, size: float) -> list[Surface]:
    loaded_assets = []
    asset_dir = resource_path(f"src/assets/{name}_assets")
    files = sorted(asset_dir.glob(f"{name}_{direction}*.png"),
                   key=frame_number)
    for i in files:
        image = pygame.image.load(str(i)).convert_alpha()
        loaded_assets.append(pygame.transform.scale_by(image, 20 / size))
    return loaded_assets
