## Timeline

For progress tracking and task cards, refer to our [Trello Board](https://trello.com/b/Z480iQSZ/to-dos).

### Week 1:
- **Project Setup and documentation (Weng):** Makefile, pyproject.toml, package dependencies and project management tracking README.md, project_management/
- **Configuration & Maze Loading (Weng):** `ConfigParser` (src/parser.py) with validation/defaults, `MazeLoader` (src/maze_loader.py) integrating the external mazegenerator wheel
- **Window & Maze Rendering (Jenny):** Pygame window initialization and neon wall rendering from bitmask grids (src/drawmaze.py)
- **Player & Menu Basics (Jenny & Weng):** Pac-Man spawning, sprite animations, and keyboard bindings (src/pacman.py, src/asset_helper.py by Jenny); initial `GameMenu` (src/menu.py by Weng)

### Week 2:
- **Highscores & State Machine (Weng):**
  - `HighscoreRecord` JSON persistence and validation (src/highscores.py)
  - Interactive Pygame `Leaderboard` and `NameInput` screens with live input validation and `score_saved` confirmation
  - `GameManager` state machine (`MENU` -> `PLAYING` -> `NAME_INPUT` -> `HIGHSCORES` -> `QUIT`) in src/game_manager.py
  - Custom arcade styling for `GameMenu` (src/menu.py)
  - Project documentation and project management tracking (README.md, project_management/)
- **Gameplay Entities (Jenny):**
  - `Pacgum` random distribution and collision detection (src/pacgum.py)
  - `Ghosts` corner spawning and target tracking (src/ghosts.py)
  - Start/pause mechanics (src/player_mechanics.py)

### Week 3:
- ** Planned (Weng):**
  - `MazeLoader` fallback generator (src/maze_loader.py)
  - Merging gameplay loop (`DrawMaze`) into `GameManager._handle_playing`
  - Level progression and difficulty scaling (ghost speed, pacgum count, default levels fallback)

## Phases

1. **Phase 1 — Setup & Data Layer:** Repository structure, `ConfigParser`, `MazeLoader`, `HighscoreRecord`
2. **Phase 2 — Core Rendering & UI Screens:** `DrawMaze`, `PacMan` controls, `GameMenu` design, `Leaderboard`, `NameInput`, `GameManager` state loop
3. **Phase 3 — Gameplay Mechanics & Fallback Robustness:** Ghost AI/movement, pacgum scoring, `MazeLoader` fallback grid, default level configs
4. **Phase 4 — Full Integration & Polish:** Connecting `DrawMaze` into `GameManager._handle_playing`, multi-level progression, final testing & documentation

## Planned vs Actual

| Milestone | Planned | Actual | Notes |
| --- | --- | --- | --- |
| Config & Maze Loader | Week 1 | Done in Week 1 | Added square-grid enforcement; adding fallback maze next |
| Menu, Leaderboard & NameInput | Week 1–2 | Done in Week 2 | Replaced terminal prompts with full Pygame `NameInput` + `Leaderboard` screens and unified dark arcade theme |
| Pac-Man, Pacgums & Ghosts | Week 1–2 | In Progress | Pac-Man movement and pacgum collisions working; ghost movement/AI |
| Game-to-Menu Integration | Week 2 | In Progress | Connect gameplay mechanics with the menu |
