from pathlib import Path
import pygame


def asset_loader(name: str, direction: str, size: int):

    loaded_assets = []
    asset_dir = Path(f"src/assets/{name}_assets")
    files = sorted(asset_dir.glob(f"{name}_{direction}*.png"))
    for i in files:
        image = pygame.image.load(str(i)).convert_alpha()
        loaded_assets.append(pygame.transform.scale_by(image, 20 / size))
    return loaded_assets
