*This project has been created as part of the 42 curriculum by jtruckse, wcheung.*

### Description

A 2D Pac-Man game built with Python and Pygame as part of the 42 curriculum. Features dynamic mazes loaded from an external generator wheel, ghost AI, multi-level progression, persistent highscores, and an arcade-style menu.

### Instructions

#### Requirements
- Python 3.12+
- `uv` package manager

#### Setup & Run
- Install dependencies and wheel package:
  ```bash
  make install
  ```
- Run the game:
  ```bash
  make run
  ```
  Or directly:
  ```bash
  uv run python3 pac-man.py config.json
  ```

#### Controls
- **Menu:**
  - `W` / `S` or `Up` / `Down`: Navigate buttons
  - `Space` or `Enter`: Select option
- **In-Game:**
  - `W` / `A` / `S` / `D` or `Arrow Keys`: Move Pac-Man
  - `Space`: Start / Pause game
  - `Escape`: Return to menu
- **Cheat Mode:**
  - `C`: Toggle cheat mode
  - `T`: Freeze timer
  - `L`: Reset lives to 3
  - `N`: Skip level / Win
  - `X`: Exit cheat mode
- **Highscores Screen:**
  - Type name (up to 10 characters, alphanumeric and spaces)
  - `Backspace`: Delete character
  - `Enter`: Submit score
  - `Escape` or `Space`: Return to menu from leaderboard




### Configuration

The game is configured via a JSON file (e.g. `config.json`):

| item | description | data type | default value |
| --- | --- | --- | --- |
| `highscore_filename` | The file name (or path) where top 10 highscores are stored | str | `"highscores.json"` |
| `seed` | Seed used for random maze generation and reproducibility | int | `42` |
| `lives` | Number of chances before game over | int | `3` |
| `level_max_time` | Maximum time allowed per level in seconds | int | `90` |
| `pacgum` | Number of pacgums spawned in each level | int | `42` |
| `points_per_pacgum` | Score points per eaten pacgum | int | `10` |
| `points_per_super_pacgum` | Score points per eaten super pacgum | int | `50` |
| `points_per_ghost` | Score points per eaten ghost | int | `200` |
| `levels` | List of level config with `level`, `width`, and `height` | list[dict] | `[{"level": 1, "width": 20, "height": 20}]` |


A demo of config.json:

    {
        "highscore_filename": "highscores.json",
        "seed": 42,
        "lives": 3,
        "level_max_time": 90,
        "pacgum": 42,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "levels": [
            {
                "level": 1,
                "width": 15,
                "height": 15
            },
            {
                "level": 2,
                "width": 15,
                "height": 15
            },
            {
                "level": 3,
                "width": 17,
                "height": 17
            },
            {
                "level": 4,
                "width": 17,
                "height": 17
            },
            {
                "level": 5,
                "width": 19,
                "height": 19
            },
            {
                "level": 6,
                "width": 19,
                "height": 19
            },
            {
                "level": 7,
                "width": 21,
                "height": 21
            },
            {
                "level": 8,
                "width": 23,
                "height": 23
            },
            {
                "level": 9,
                "width": 23,
                "height": 23
            },
            {
                "level": 10,
                "width": 25,
                "height": 25
            }
        ]
    }


### Highscore
The highscore system persists player scores across game sessions (`src/highscores.py`).

- **Storage Format:** Stored as a simple JSON list at the path specified by `"highscore_filename"` in `config.json` (defaults to `highscores.json`)
- **Data Validation & Constraints (`HighscoreRecord`):**
  - Player names: 1 to 10 characters, restricted to alphanumeric characters and spaces
  - Scores: Non-negative integers (`score >= 0`)
  - Top 10 Highscores: Maintained in descending order of score, keeping at most the top 10 entries
- **Robustness & Error Handling:**
  - Missing, empty, or corrupted files gracefully fall back to an empty list without crashing
  - Malformed or invalid entries are discarded during loading
- **Interactive Pygame Screens (`Leaderboard` & `NameInput`):**
  - **`Leaderboard`:** Displays the top 10 ranked players and scores directly in the Pygame window, accessible from the main menu or after submitting a score
  - **`NameInput`:** Interactive post-game screen where players type their name with live character/length validation, on-screen error feedback, and a confirmation screen (`score_saved`) before transitioning to the leaderboard

### Maze Generation
Mazes are generated dynamically via `MazeLoader` (`src/maze_loader.py`) using the external `mazegenerator` package (`A-Maze-ing` wheel):

- **Generator Configuration:**
  - `MazeLoader.load(width, height, seed)` instantiates `MazeGenerator(size=(width, height), entry_cell=(0, 0), exit_cell=(0, 0), perfect=False, seed=seed)`
  - Setting `perfect=False` creates loops and multiple paths rather than dead-end-heavy perfect mazes, which is essential for Pac-Man gameplay so the player can evade ghosts
  - Dimensions (`width`, `height`) are read per level from `config.json` (enforced as square grids up to `25x25`), and `seed` ensures reproducible layouts
- **Wall Bitmask Encoding:**
  - Each cell in `MazeData.grid` (`list[list[int]]`) stores an integer bitmask (`0`–`15`) representing which walls surround that cell:
    - `1` (`UP` / Top wall)
    - `2` (`RIGHT` / Right wall)
    - `4` (`DOWN` / Bottom wall)
    - `8` (`LEFT` / Left wall)
  - `DrawMaze` (`src/drawmaze.py`) and `PacMan` (`src/pacman.py`) use bitwise AND (`cell & direction`) to render walls and check valid movement directions
- **Robust Error Handling & Subject V.4 Compliance:**
  - In strict compliance with 42 Subject Section V.4 (*"You must not write your own generator... Your loader must adapt to their interface, not the opposite. If the generator fails, you must handle the error cleanly."*), the project does not generate custom mazes.
  - If the external `mazegenerator` wheel is missing, crashes, or returns an invalid grid, `MazeLoader` raises a custom `MazeLoaderError`.
  - `GameManager` catches this error cleanly, presents an on-screen/console warning, and returns safely to the main menu without crashing.
- **Dynamic Spawn Placement (`_find_spawn_cell`):**
  - Mazes with dimensions $\ge 14 \times 10$ generated by the assigned wheel embed a solid $5 \times 7$ "42" pattern (cells set to `15` / all four walls closed) at the center.
  - `DrawMaze` dynamically checks the spawn cell: if solid (`15`), it steps left until an open, walkable cell is found, ensuring Pac-Man never spawns trapped inside obstacle walls.

### Implementation

- **Architecture:** Centralized finite state machine (`GameManager`) controlling transitions between `MENU`, `PLAYING`, `NAME_INPUT`, `HIGHSCORES`, and `QUIT`
- **Maze Integration:** Interfaces with external `mazegenerator` wheel, parses wall bitmasks (`1: UP, 2: RIGHT, 4: DOWN, 8: LEFT`), and cleanly handles wheel errors via `MazeLoaderError`
- **Player & Collision:** Grid-aligned movement with bitwise wall checks preventing movement into closed cells
- **Ghost AI & States:** Ghosts spawn at corners, chase Pac-Man, and switch to frightened/flee behavior when super-pacgums are eaten
- **Scoring & Lives:** Real-time scoring from pacgums, super-pacgums, and eaten ghosts; player lives tracking with countdown timer per level
- **Leaderboard:** Persistent JSON storage preserving top 10 scores with in-game name entry and input sanitization

### General Software Architecture

#### Project Structure
```text
pacman/
├── pac-man.py                  # Entry point: CLI validation, ConfigParser -> GameManager
├── config.json                 # Game & level configuration
├── highscores.json             # Persistent Top-10 leaderboard storage
├── assets/                     # Directional sprite sheets (Pac-Man, Ghosts)
├── project_management/         # Team roles, phases & timeline tracking
└── src/
    ├── parser.py               # ConfigParser, GameConfig, LevelsConfig
    ├── game_manager.py         # GameManager & GameState state machine
    ├── menu.py                 # GameMenu (pygame_menu main menu UI)
    ├── highscores.py           # HighscoreRecord, NameInput, Leaderboard
    ├── maze_loader.py          # MazeLoader, MazeData (A-Maze-ing wheel integration)
    ├── drawmaze.py             # DrawMaze (maze wall rendering & game loop)
    ├── player_mechanics.py     # Game (start/pause state controller)
    ├── pacman.py               # PacMan (grid movement, wall checks, animation)
    ├── pacgum.py               # Pacgum (distribution & collision detection)
    ├── ghosts.py               # Ghosts (Blinky, Pinky, Inky, Clyde targeting)
    └── asset_helper.py         # Sprite loader helper
```
The application is driven by a central state machine in `GameManager` (`src/game_manager.py`) using `GameState`:
- `pac-man.py` — Entry point: validates CLI arguments, parses `config.json` via `ConfigParser`, and launches `GameManager`
- `src/game_manager.py` — Central controller managing the Pygame window, clock, and transitions between `GameState.MENU`, `GameState.PLAYING`, `GameState.NAME_INPUT`, `GameState.HIGHSCORES`, and `GameState.QUIT`
- `src/menu.py` — `GameMenu`: main menu UI returning `"PLAY"`, `"HIGHSCORES"`, or `"QUIT"`
- `src/highscores.py` — `HighscoreRecord` (JSON persistence & validation), `NameInput` (post-game name entry UI), and `Leaderboard` (top-10 display UI)
- `src/maze_loader.py` — `MazeLoader` & `MazeData`: wrapper around `MazeGenerator` with validation and clean error handling
- `src/drawmaze.py`, `src/pacman.py`, `src/pacgum.py`, `src/ghosts.py`, `src/player_mechanics.py` — Maze rendering, Pac-Man movement/animation, pacgum distribution/collision, and ghost mechanics

#### State Flow Diagram
```text
                        ┌──────────────────────┐
                        │      pac-man.py      │
                        └──────────┬───────────┘
                                   │ parses config.json
                                   ▼
                        ┌──────────────────────┐
                        │     ConfigParser     │
                        └──────────┬───────────┘
                                   │ GameConfig
                                   ▼
                        ┌──────────────────────┐
                        │     GameManager      │
                        └──────────┬───────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   GameState   │   Play   │   GameState   │ Game End │   GameState   │
│     MENU      ├─────────►│    PLAYING    ├─────────►│  NAME_INPUT   │
│  (GameMenu)   │          │  (DrawMaze)   │          │  (NameInput)  │
└───────┬───────┘          └───────┬───────┘          └───────┬───────┘
        │                          │                          │
        │ Highscores               ├─► MazeLoader             │ Submit Score
        │                          ├─► PacMan                 ▼
        │                          ├─► Pacgum         ┌───────────────┐
        │                          └─► Ghosts         │   GameState   │
        └────────────────────────────────────────────►│  HIGHSCORES   │
                                                      │ (Leaderboard) │
                                                      └───────────────┘
```


### Project Management

We track progress, weekly sprints, and task division in the [project_management/](project_management/) directory:
- [project_management/README.md](project_management/README.md): Team responsibilities and tools
- [project_management/timeline.md](project_management/timeline.md): Weekly tasks, development phases, and planned vs. actual tracking
- [project_management/risks.md](project_management/risks.md): Risk analysis and mitigations
- [project_management/bugs.md](project_management/bugs.md): Bugs found/fixed and acceptance tests
- [Trello Board](https://trello.com/b/Z480iQSZ/to-dos): Sprint to-dos and task cards

### Resources
