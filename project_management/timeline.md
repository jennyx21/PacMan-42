## Timeline

For progress tracking and task cards, refer to our [Trello Board](https://trello.com/b/Z480iQSZ/to-dos).

### Week 1:
- **Weng:**
  - Project setup: Makefile, pyproject.toml, package dependencies, and project management tracking (README.md, project_management/)
  - `ConfigParser` (src/parser.py) with validation and defaults
  - `MazeLoader` (src/maze_loader.py) integrating the external mazegenerator wheel
  - Initial `GameMenu` (src/menu.py)
- **Jenny:**
  - Pygame window initialization and neon wall rendering from bitmask grids (src/drawmaze.py)
  - Pac-Man spawning, sprite animations, and keyboard bindings (src/pacman.py, src/asset_helper.py)

### Week 2:
- **Weng:**
  - `HighscoreRecord` JSON persistence and validation (src/highscores.py)
  - Interactive Pygame `Leaderboard` and `NameInput` screens with live input validation and `score_saved` confirmation
  - `GameManager` state machine (MENU -> PLAYING -> NAME_INPUT -> HIGHSCORES -> QUIT`) in src/game_manager.py
  - Custom arcade styling for `GameMenu` (src/menu.py)
  - Project documentation and project management tracking (README.md, project_management/)
- **Jenny:**
  - `Pacgum` random distribution and collision detection (src/pacgum.py)
  - `Ghosts` corner spawning and target tracking (src/ghosts.py)
  - Start/pause mechanics (src/player_mechanics.py)

### Week 3:
- **Weng:**
  - `MazeLoader` fallback generator DFS (src/maze_loader.py)
  - Merging gameplay loop into `GameManager._handle_playing`
  - Level progression and difficulty scaling (ghost speed, pacgum count, default levels fallback)
- **Jenny:**
  - Add a state to mark `Ghosts` as edible when superpacgum is eaten
  - Point system that sends score as an int value to highscores
  - `Ghosts` edible by pacman and flee algorithm
  - Implement ghost classes (Pinky, Inky, Clyde)

### Week 4:
- **Weng:**
  - Change `MazeLoader` fallback generator algorithm first and then decided not to put a fallback maze (src/maze_loader.py)
  - Fix highscores.py to reject spaces-only input
  - Display top 3 on main menu
  - Makefile fix (lint and lint-strict)
  - Refactor `DrawMaze` class
  - Add an instruction page to menu
- **Jenny:**
  - `Ghosts` are edible now
  - Implemented player lose lives
  - Display score and remaining lives, and add draw maze to game manager
  - Implemented cheat mode
  - Implemented timer and timer bar that runs down
  - Drawing the main menu and instruction pages
  - Animated menu
  - FIxes for Mypy and flake8
  - Publish on Itch.io

## Phases

1. **Phase 1 — Setup & Data Layer:** Repository structure, `ConfigParser`, `MazeLoader`, `HighscoreRecord`
2. **Phase 2 — Core Rendering & UI Screens:** `DrawMaze`, `PacMan` controls, `GameMenu` design, `Leaderboard`, `NameInput`, `GameManager` state loop
3. **Phase 3 — Gameplay Mechanics & Fallback Robustness:** Ghost AI/movement, pacgum scoring, `MazeLoader` fallback grid, default level configs
4. **Phase 4 — Full Integration & Polish:** Connecting `DrawMaze` into `GameManager._handle_playing`, multi-level progression, final testing & documentation, package the game and launch on a public platform (we chose Itch.io)

## Planned vs Actual

| Milestone | Planned | Actual | Notes |
| --- | --- | --- | --- |
| Config & Maze Loader | Week 1 | Done in Week 1 | Added square-grid enforcement and wheel interface |
| Menu, Leaderboard & NameInput | Week 1–2 | Done in Week 2 | Pygame `NameInput` + `Leaderboard` screens with arcade theme |
| Pac-Man, Pacgums & Ghosts | Week 1–2 | Done in Week 3–4 | Movement, collisions, edible ghosts, and lives system |
| Game-to-Menu Integration | Week 2 | Done in Week 3 | Connected `DrawMaze` to `GameManager._handle_playing` |
| Fallback Maze vs Subject V.4 | Week 3 | Scrapped in Week 4 | Tested DFS and Prim's, but removed fallback generator to strictly comply with Subject V.4; handle wheel errors cleanly with `MazeLoaderError` |
| 42 Pattern Spawn Fix | Week 4 | Done in Week 4 | Added helper to shift spawn left when cell is a 4-wall obstacle |
| Menu Top 3 & Polish | Week 4 | Done in Week 4 | Top 3 scores shown on menu; rejected spaces-only input; timer bar and dim overlays |
