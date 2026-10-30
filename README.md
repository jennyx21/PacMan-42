*This project has been created as part of the 42 curriculum by jtruckse, wcheung.*

### Description


### Instructions




### Configuration
explaining the config file structure and default values

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
- **Fallback Handling:**
  - If the external `mazegenerator` wheel is missing, crashes, or returns a malformed grid, `MazeLoader` falls back to an internal fallback maze generator (`_fallback_maze`) so the game remains playable

### Implementation
a technical summary of your implementation

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
    ├── maze_loader.py          # MazeLoader, MazeData (A-Maze-ing wrapper + fallback)
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
- `src/maze_loader.py` — `MazeLoader` & `MazeData`: wrapper around `MazeGenerator` with validation and fallback support
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
with a brief overview of how you managed the project and a link to the dedicated project management directory

### Resources
