from pathlib import Path
import pygame 


def asset_loader(name: str, direction: str):

    loaded_assets = []
    asset_dir = Path(f"src/assets/{name}_assets")
    print(asset_dir)
    files = sorted(asset_dir.glob(f"{name}_{direction}*.png"))
    print(files)
    for i in files:
        print(i)
        loaded_assets.append(pygame.image.load(str(i)))

    return loaded_assets
