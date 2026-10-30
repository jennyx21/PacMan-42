## Project Management

This directory tracks task breakdown, development phases, and planned vs. actual progress for the Pac-Man project by Jenny (`jtruckse`) and Weng (`wcheung`).

## Directory Structure

    project_management/
    ├── README.md                  # Index of project management
    └── timeline.md                # Tracking planned vs. actual progress

## Team Responsibilities

- **Weng**: 
Project setup (`Makefile`, `pyproject.toml`), 
`ConfigParser` (`src/parser.py`), 
`MazeLoader` & fallback (`src/maze_loader.py`), 
`HighscoreRecord` / `Leaderboard` / `NameInput` (`src/highscores.py`), 
`GameMenu` (`src/menu.py`), 
`GameManager` state machine (`src/game_manager.py`), 
and project documentation (`README.md`, `project_management/`)
- **Jenny**: 
Maze wall rendering (`src/drawmaze.py`), 
sprite asset loading (`src/asset_helper.py`), 
`PacMan` movement & collision (`src/pacman.py`), 
`Pacgum` spawning & collection (`src/pacgum.py`), 
`Ghosts` AI & mechanics (`src/ghosts.py`), 
and game state controls (`src/player_mechanics.py`)
