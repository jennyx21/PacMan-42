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
The highscore system persists player scores across game sessions.

- **Storage Format:** Stored as a simple JSON list at the path specified by `"highscore_filename"` in `config.json` (defaults to `highscores.json`).
- **Data Validation & Constraints:**
  - Player names: 1 to 10 characters, restricted to alphanumeric characters and spaces.
  - Scores: Non-negative integers (`score >= 0`).
  - Top 10 Highscores: Maintained in descending order of score, keeping at most the top 10 entries.
- **Robustness & Error Handling:**
  - Missing, empty, or corrupted files gracefully fall back to an empty list without crashing.
  - Malformed or invalid entries are discarded during loading.
- **Lifecycle & User Experience:**
  - Loaded automatically at game start and saved when scores are added or when the game exits.
  - Displayed in the main menu before starting a game.
  - When a game ends (win or lose), players are prompted to enter their name.

### Maze Generation
explaining how the assigned A-Maze-ing package is used to generate mazes

### Implementation
a technical summary of your implementation

### General Software Architecture
with high-level overview of the software architecture (modules, classes, and their relationships)

### Project Management
with a brief overview of how you managed the project and a link to the dedicated project management directory

### Resources
