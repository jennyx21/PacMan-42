from pathlib import Path
import pygame


def asset_loader(name: str, direction: str):

    loaded_assets = []
    asset_dir = Path(f"src/assets/{name}_assets")
    files = sorted(asset_dir.glob(f"{name}_{direction}*.png"))
    for i in files:
        loaded_assets.append(pygame.image.load(str(i)).convert_alpha())

    return loaded_assets
