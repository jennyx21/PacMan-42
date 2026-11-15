## Risk Analysis & Mitigation

| Risk | Impact | Mitigation |
| --- | --- | --- |
| **External wheel fails or missing** | Cannot load maze; peer review re-installs wheel | Catch errors in `MazeLoader`, raise `MazeLoaderError`, return cleanly to menu instead of crashing. Scrapped custom generator to strictly follow Subject V.4. |
| **Pac-Man spawns in obstacle wall** | Player stuck inside "42" pattern cell (`15`) on dimensions $\ge 14\times 10$ | Helper `_find_spawn_cell()` checks if center cell has 4 walls; if yes, shifts left until walkable cell found. |
| **Maze is too hard to play/ too many deadends** | Even with `perfect=False`, maze layout can be too difficult to clear in time | Built-in cheat mode for testing and evaluation (`c` enables cheat mode: `l` resets lives, `t` freezes timer, `n` skips level, `x` exits). |
| **Corrupted or missing highscore file** | Game crash on launch | Catch `FileNotFoundError` and `JSONDecodeError` in `HighscoreRecord.load()`, fallback to empty list. |
